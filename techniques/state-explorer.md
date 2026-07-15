---
id: techniques.state-explorer
title: 상태 탐색기 (커버리지 % 자동 측정)
doctype: technique
status: verified
proven_in: [canvas]
related: [techniques.rip-crawler, techniques.state-spec-json, pipelines.99-percent]
evidence:
  - "260615_canvas-clone ref/_RIP_EXPLORE_PILOT.md (2026-07-14) — 프론티어 큐 BFS 파일럿: 사람 미열거 신규 상태 자동 발견(opus 보정 후 6패밀리, 기준 ≥5)·커버리지 % 산출(실물 8.7%/클론 7.2%)·안전 무사고. ⚠조건부: novelty 분류기 실물측 맹점(AA-D1) 보강이 필수 후속(ref/_VERIFY_r1.md §AA)"
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md §4, §6 — 판정식 항목①(상태 커버리지 ≥95%), 파일럿 승격 기준: '사람이 열거 안 한 신규 상태 ≥5개 자동 발견'"
  - "260615_canvas-clone 커밋 6354f61(2026-07-16, 세션17) — 프론티어 1패스를 measure-only로 축소 운용, §10 갭후보 목록만 산출(라이브 재검증 전 갭 미확정)"
updated: 2026-07-16
owner: 박춘순
---

# 상태 탐색기 (커버리지 % 자동 측정)

**한 줄**: "우리가 아직 못 본 UI 상태가 몇 % 남았나"를 사람의 열거가 아니라 도구가 스스로 발견하고 % 숫자로 답하게 만드는 도구. canvas 99% 판정식의 항목①(상태 커버리지 ≥95%)을 채우기 위한 개념.

## 상태: 개념 정의됨, 도구 미완성
[[techniques.rip-crawler]]가 "지정된 상태에서" 인터랙션을 전수 탐색하는 것과 달리, state-explorer는 "**아직 지정 안 된 상태 자체를 발견**"하는 상위 개념이다. 승격 기준으로 "사람이 열거 안 한 신규 상태 ≥5개 자동 발견"이 명시되어 있으나 2026-07-13 기준 아직 이 기준을 통과한 실행 기록이 없음.

## rip-crawler와의 관계 (가장 가까운 구현 후보)
kit/canvas의 `rip_dump.py`/`rip_align.py`/`rip_crawl.py` 조합이 사실상 이 개념의 프로토타입에 가깝다 — 다만 "커버리지 %"라는 명시적 지표를 아직 산출하지 않는다. 승격하려면 rip-crawler의 상태그래프에서 "전체 대비 몇 %를 커버했나"를 계산하는 로직이 추가되어야 함.

## 함정 — `--resume` 스테일 trigger-text (2026-07-16 세션17)
탐사기를 이전 세션 상태그래프에서 `--resume`으로 이어 돌릴 때, 클론 쪽 그래프가 **몇 세션 전 캡처 시점의 trigger-text(클릭 대상 라벨)를 그대로 이고 있는** 경우가 있다. 그 사이 클론 코드가 바뀌어(라벨 변경·구조 수복 등) 실제로는 이미 존재/수복된 상태인데, 스테일 trigger-text 기준으로 diff하면 "클론에 없다"는 갭으로 **과대보고**된다 — 세션16의 유령 티켓(§ledger 2026-07-15)과 같은 뿌리, 이번엔 프론티어 탐사기에서 재발할 뻔했다.

**대응**: 프론티어 재개(`--resume`) 시 이전 캡처의 trigger-text를 신뢰하지 않고, §10 같은 "갭후보" 목록으로만 잠정 등록 → **라이브 재검증(실물+클론 양쪽 실측) 없이는 갭으로 확정하지 않는다**. measure-only 1패스로 범위를 좁혀 운용한 것이 이번엔 과대보고를 실제 발생 전에 걸렀다.

## 관련
- [[techniques.rip-crawler]] — 가장 가까운 기존 구현, 이 기법의 토대가 될 후보
- [[techniques.rip-repair-loop]] — 스테일 큐가 유령 티켓을 만드는 동일 패턴(§근본수정 사례)
- [[pipelines.99-percent]] — 판정식 항목①
