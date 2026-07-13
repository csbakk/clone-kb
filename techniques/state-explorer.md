---
id: techniques.state-explorer
title: 상태 탐색기 (커버리지 % 자동 측정)
doctype: technique
status: experimental
proven_in: []
related: [techniques.rip-crawler, techniques.state-spec-json, pipelines.99-percent]
evidence:
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md §4, §6 — 판정식 항목①(상태 커버리지 ≥95%), 파일럿 승격 기준: '사람이 열거 안 한 신규 상태 ≥5개 자동 발견'"
updated: 2026-07-13
owner: 박춘순
---

# 상태 탐색기 (커버리지 % 자동 측정)

**한 줄**: "우리가 아직 못 본 UI 상태가 몇 % 남았나"를 사람의 열거가 아니라 도구가 스스로 발견하고 % 숫자로 답하게 만드는 도구. canvas 99% 판정식의 항목①(상태 커버리지 ≥95%)을 채우기 위한 개념.

## 상태: 개념 정의됨, 도구 미완성
[[techniques.rip-crawler]]가 "지정된 상태에서" 인터랙션을 전수 탐색하는 것과 달리, state-explorer는 "**아직 지정 안 된 상태 자체를 발견**"하는 상위 개념이다. 승격 기준으로 "사람이 열거 안 한 신규 상태 ≥5개 자동 발견"이 명시되어 있으나 2026-07-13 기준 아직 이 기준을 통과한 실행 기록이 없음.

## rip-crawler와의 관계 (가장 가까운 구현 후보)
kit/canvas의 `rip_dump.py`/`rip_align.py`/`rip_crawl.py` 조합이 사실상 이 개념의 프로토타입에 가깝다 — 다만 "커버리지 %"라는 명시적 지표를 아직 산출하지 않는다. 승격하려면 rip-crawler의 상태그래프에서 "전체 대비 몇 %를 커버했나"를 계산하는 로직이 추가되어야 함.

## 관련
- [[techniques.rip-crawler]] — 가장 가까운 기존 구현, 이 기법의 토대가 될 후보
- [[pipelines.99-percent]] — 판정식 항목①
