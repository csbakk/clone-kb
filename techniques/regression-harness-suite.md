---
id: techniques.regression-harness-suite
title: 번호매김 회귀 검증 스위트 (_bN_verify.py / *_gate.py)
doctype: technique
status: standard
proven_in: [canvas, notion, akiflow]
related: [techniques.adversarial-verification, techniques.append-only-logging, pipelines.verify-first-loop]
evidence:
  - "260615_canvas-clone/harness/_b1_verify.py ... _b11_verify.py, _bug1/_bug2_verify.py, _na_verify.py, _s2fix_verify.py — 기능/버그 단위 번호매김 검증 스크립트 다수, npx vitest run 37 tests 병행"
  - "260622_notion-clone/harness/*_gate.py — colresize_gate, columnedit_gate, columns_gate, date_gate, dragmenu_gate, dragselect_gate, editor_fixes_gate, formula_datemath_gate 등, click_audit.py 501/501 PASS"
  - "260622_akiflow-clone/harness/gate.py — 'GATE PASS 3/3'(parity 24/24 · flow 56/56 · glyph mismatch 0), tsc 0 errors"
updated: 2026-07-13
owner: 박춘순
---

# 번호매김 회귀 검증 스위트 (_bN_verify.py / *_gate.py)

**한 줄**: 기능/버그 하나마다 전용 검증 스크립트를 하나씩 쌓는다. 이후 세션에서 "이거 다시 안 깨졌는지" 전부 재실행 가능하게.

## 언제 쓰나
버그를 고치거나 기능을 붙일 때마다. "이번에 고쳤다"로 끝내지 않고, 그 수정을 검증하는 스크립트를 남겨서 다음 세션·다음 리팩터에서도 자동 회귀 검증에 편입시킨다.

## 3캠페인의 실제 형태 (이름은 다르지만 같은 패턴)
- **canvas**: `harness/_b1_verify.py` ~ `_b11_verify.py`(기능 단위, 예: `_b1`=노드 상태머신 hover/selected, `_b5`=생성중 3단계 배지), `_bug1/_bug2_verify.py`(버그 단위), `_s2fix_verify.py`. 여기에 `npx vitest run` 37개 유닛 테스트가 항상 병행 — worklog에 "37/37" 반복 확인.
- **notion**: `*_gate.py` 파일이 기능별로 다수(`colresize_gate.py`, `columnedit_gate.py`, `date_gate.py`, `dragselect_gate.py`, `formula_datemath_gate.py` 등) — canvas의 번호 대신 기능명을 파일명에 직접 박음. `click_audit.py`는 전체 클릭 표면을 도는 종합 감사 스크립트로 최신 회귀에서 **501/501 PASS**.
- **akiflow**: `harness/gate.py`가 parity+flow+glyph 세 축을 한 번에 묶어 "GATE PASS 3/3" 단일 출력으로 통합 — 개별 게이트를 상위 게이트가 합산하는 형태로 한 단계 더 진화.

## 왜 필요한가
클론 캠페인은 세션이 수십~수백 번 이어진다. 사람이 매번 "이 버그 안 재발했나?"를 손으로 재확인하는 건 불가능 — 스크립트로 남겨야 다음 세션(특히 무인 야간 런)이 자동으로 회귀를 잡는다.

## 함정
- 검증 스크립트가 빌더 자신이 짠 것이면 빌더의 맹점을 그대로 물려받는다 → 가능하면 [[techniques.adversarial-verification]] 원칙과 결합(검증 스크립트는 "빌더의 주장"이 아니라 "독립 재측정"이어야 함).
- 스크립트 개수가 늘어나면 전체 실행 시간이 길어진다 — akiflow의 `gate.py`처럼 상위 통합 게이트로 묶어 한 번에 PASS/FAIL 요약을 내는 게 확장성에 좋다.

## 관련
- [[techniques.append-only-logging]] — 검증 통과/실패 이력을 남기는 짝 기법
