---
id: techniques.parity-ci
title: 파리티 CI (교차앱 자동 회귀 파이프라인)
doctype: technique
status: experimental
proven_in: []
related: [techniques.regression-harness-suite, techniques.parity-watch-daemon]
evidence:
  - "260615_canvas-clone HANDOFF.md/worklog — GitHub Actions로 build + npx vitest run(37 tests) 상시 CI 운영 중이나, 이건 단일 리포 빌드검증이지 '파리티(실물과의 일치도) CI'는 아님"
updated: 2026-07-13
owner: 박춘순
---

# 파리티 CI (교차앱 자동 회귀 파이프라인)

**한 줄**: "파리티 CI"라는 이름에 걸맞게, PR/커밋마다 [[techniques.rip-css-dump]]·[[techniques.rip-crawler]] 같은 실물 대조 검증까지 자동으로 돌리는 CI를 만들려는 개념. 아직 이 수준까지는 구현되지 않았다.

## 현재 실제로 있는 것 (혼동 주의)
canvas-clone 리포는 GitHub Actions로 **build + `npx vitest run`(37개 유닛테스트)**을 상시 CI로 돌리고 있다. 이건 "코드가 안 깨졌는지" 검증이지, "실물 앱과의 파리티가 유지되는지"를 검증하는 CI가 아니다 — 후자가 이 카드가 가리키는 목표.

## 왜 experimental로 분류했나
이름이 가리키는 목표(파리티 유지 자동검증)와 현재 존재하는 구현(빌드/유닛테스트 CI) 사이에 갭이 크다. RIP 파이프라인 같은 실물 대조 도구는 실물 세션·CDP·시간이 걸리는 작업이라 일반 CI 러너에 그대로 얹기 어렵다는 현실적 난관도 있음 — 아직 아무도 이 통합을 설계하지 않았다.

## 관련
- [[techniques.regression-harness-suite]] — CI에서 돌아가는 기존 검증 스위트(빌드/유닛테스트 한정)
- [[techniques.parity-watch-daemon]] — 유사한 미해결 목표(상시 파리티 재확인)와 겹치는 지점 있음, 스케줄 데몬 vs PR 트리거 CI로 접근 방식이 다를 뿐
