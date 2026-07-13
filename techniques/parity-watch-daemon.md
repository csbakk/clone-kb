---
id: techniques.parity-watch-daemon
title: 파리티 감시 데몬 (99% 선언 이후 유지)
doctype: technique
status: experimental
proven_in: []
related: [pipelines.99-percent, techniques.parity-ci]
evidence:
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md §4 — '전항 충족 → 99% 선언 + 감시 데몬으로 유지', 2026-07-13 기준 개념만 존재"
updated: 2026-07-13
owner: 박춘순
---

# 파리티 감시 데몬 (99% 선언 이후 유지)

**한 줄**: 6축 판정식([[pipelines.99-percent]])을 전부 통과해 "99% 파리티" 선언을 한 뒤, 실물 앱이 계속 업데이트되며 다시 벌어지는 갭을 상시 감시하려는 개념.

## 상태: 개념만, 미구현
canvas 99% 계획 문서에 "전항 충족 → 99% 선언 + 감시 데몬으로 유지"라고 한 줄 언급되어 있을 뿐, 어떤 주기로 무엇을 재실행할지 등 구체 설계는 아직 없음.

## 가장 가까운 기존 구현 (참고, 동일 기법 아님)
canvas 리포는 이미 GitHub Actions로 build+vitest CI를 상시 돌리고 있다(→ [[techniques.parity-ci]]). 감시 데몬은 이걸 "빌드가 깨졌는지"가 아니라 "**실물과의 파리티가 다시 벌어졌는지**"를 주기적으로 재측정하는 방향으로 확장하는 것 — 아직 그 확장은 실행되지 않음.

## 관련
- [[techniques.parity-ci]] — 가장 가까운 기존 CI 구현(빌드/유닛테스트 한정, 파리티 재측정은 아직 없음)
