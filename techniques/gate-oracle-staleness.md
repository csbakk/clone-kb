---
id: techniques.gate-oracle-staleness
title: 게이트 FAIL ≠ 클론 버그 — 게이트 오라클도 낡는다
doctype: technique
status: experimental
proven_in: [notion]
related: [techniques.regression-harness-suite, techniques.differential-conformance-pipeline, techniques.adversarial-verification]
evidence:
  - "260622_notion-clone/_TICKETS.md §0721 무인런 — block_delete 6a/6c/6d ★오판정 정정"
  - "260622_notion-clone commit 258c59e — fix(harness): block_delete_gate 케이스6 오라클을 W-GT 수복 이후 real로 갱신"
  - "260622_notion-clone commit c036ed7 — tickets: block_delete 6a/6c/6d 오판정 정정(W-IR 반박 수용)"
  - "260622_notion-clone commit fa43740 — policy: 게이트 FAIL ≠ 클론 버그 규칙 명문화"
  - "260622_notion-clone _POLICY.md §검증 — '게이트 기대값도 낡는다' 조항"
updated: 2026-07-21
owner: 박춘순
---

# 게이트 FAIL ≠ 클론 버그 (게이트 오라클도 낡는다)

**한 줄**: 회귀 게이트가 FAIL을 뱉으면 반사적으로 "클론이 아직 안 고쳐졌다"고 단정하지 마라. **코드가 게이트보다 먼저 옳아지는** 경우(다른 워커가 real 재측정 기반으로 이미 정답으로 수복했는데 게이트 스크립트는 옛 기대값을 그대로 갖고 있는 경우)가 있고, 이때는 FAIL이 게이트의 낡은 오라클 탓이다.

## 사례 (notion, 2026-07-21 무인 런)

`block_delete_gate.py` 케이스6(fn-delete로 자식 있는 토글 삭제)이 FAIL을 냈다. 오케가 이를 곧바로 "클론 미구현"으로 단정해 수복 티켓을 발행했다 — 게이트의 기대값이 "1차 Delete=선택 상태 전환, 2차 Delete=병합"이라는 2단계 안전장치를 요구하고 있었기 때문.

워커(W-IR)가 착수 전 **real(9224)에서 직접 재측정**했다: 기존 증거(WGH04) + 오늘 재현(WIR01) 둘 다 **1회 FwdDelete로 즉시 병합**되고, 선택 상태로 전환되는 단계 자체가 real에 없었다. 즉 게이트가 요구하던 "1차 선택/2차 삭제" 오라클은 **애초에 real에 존재한 적이 없다** — 어느 세션이 잘못 측정해 게이트에 박아둔 것이었다.

클론 `Editor.tsx:2109-2116`을 확인하니 이미 이전 세션(W-GT)이 real 기준으로 정확하게 수복해둔 상태였다 — **코드는 고칠 게 없었다.** 고쳐야 했던 건 게이트 쪽: `block_delete_gate.py` 케이스6의 기대값을 real 재측정에 맞춰 갱신(그것도 완화가 아니라 **더 엄격하게** — 병합 텍스트 정확 일치·선택 상태 없음 확인을 추가)했고, 그 결과 18/18로 회귀 없이 통과했다.

## 판정 절차

FAIL을 보면 **둘 다 의심**한다 — 어느 한쪽으로 지레짐작하지 않는다:
1. 코드가 틀렸나 (진짜 파리티 갭)
2. 게이트 기대값이 낡았나 (오라클 자체가 오염되었거나 이후 수복을 못 따라감)

판정은 **real 재실측으로만** 한다. 게이트 코드나 클론 코드를 읽는 것만으로 결론내지 않는다 — 이 사례에서도 실측 2건(기존 1 + 신규 1)이 있어야 확정됐다.

## 게이트 기대값을 고쳐도 되는 경우 vs 안 되는 경우

- **정당한 변경**: real 실측 근거 + 게이트 코드/docstring에 "왜 바뀌었는지" 정정 문단을 남긴다. 이 사례처럼 변경이 **더 엄격해지는 방향**(느슨한 오라클 → real에 정확히 맞춘 오라클)인지 확인한다.
- **부당한 변경("통과시키려 낮추는 것")**: FAIL이 성가시다고 기대값을 완화해 통과시키는 것 — 이건 이 기법이 방지하려는 바로 그 실수다. 구분법: 변경 후 게이트가 이전보다 **더 관대해졌는가 더 정밀해졌는가**를 스스로 물어볼 것.

## 왜 발생하는가

무인 런처럼 여러 워커가 병렬로 서로 다른 파일을 만질 때 구조적으로 생긴다 — 한 워커(W-GT)가 코드를 real 기준으로 먼저 고치고, 그 코드를 검증하는 게이트는 그 세션의 스코프 밖이라 안 건드려진 채 남는다. 몇 세션 뒤 다른 워커/오케가 그 게이트를 돌려보면 "낡은 기대값 vs 새 정답 코드"의 충돌이 FAIL로 나타난다 — 겉보기엔 회귀처럼 보이지만 실제로는 **게이트가 과거에 멈춰 있는 것**이다.

## 관련

- [[techniques.differential-conformance-pipeline]] — 이 사건이 발견된 맥락. FE006 검증 중 W-IN이 "패치 전 HEAD로도 재현되는 기존 결함"을 발견하면서 이 게이트의 존재가 다시 도마 위에 올랐다.
- [[techniques.regression-harness-suite]] — 이 카드가 경계하는 대상인 정적 게이트(`*_gate.py`) 자체의 유지보수 문제.
- [[techniques.adversarial-verification]] — 이번엔 방향이 재밌다. 보통은 "빌더의 완료 선언을 검증자가 반박"하는 형태인데, 여기선 **오케(검증자 역할)의 FAIL 판정을 워커가 real 실측으로 반박**했다 — 적대적 검증은 계층 방향에 상관없이 적용돼야 함을 보여주는 사례.
