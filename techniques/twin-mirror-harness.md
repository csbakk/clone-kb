---
id: techniques.twin-mirror-harness
title: 트윈 미러 하네스 (실물·클론 동시 재생 비교)
doctype: technique
status: experimental
proven_in: []
related: [techniques.animation-ripper, pipelines.99-percent]
evidence:
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md §5 — P3 로드맵 '애니메이션 리퍼 → 트윈미러 하네스', 2026-07-13 기준 미착수"
updated: 2026-07-13
owner: 박춘순
---

# 트윈 미러 하네스 (실물·클론 동시 재생 비교)

**한 줄**: 같은 트리거를 실물·클론 두 탭에 동시에 흘려서 나란히 재생시키고, 프레임 단위로 대조하려는 개념 — [[techniques.animation-ripper]]가 뽑은 "지문"을 실제로 맞대어 검증하는 다음 단계.

## 상태: P3 로드맵, 미착수
2026-07-13 기준 canvas 99% 로드맵에 이름만 있고 스크립트·파일럿 실행 기록 없음.

## 가장 가까운 기존 사례 (참고용, 동일 기법은 아님)
[[techniques.adversarial-verification]]의 notion 구현(`ci_agent.py`+`ci_compare.py`)이 "같은 제스처를 실물·클론 두 탭에 동시에 흘려 DOM 변이를 대조"하는 원리는 이미 검증됨 — 트윈 미러 하네스는 이 원리를 **정적 DOM 변이가 아니라 연속 애니메이션 프레임**으로 확장하려는 것. 승격하려면 이 확장이 실제로 구현·실행되어야 함.

## 관련
- [[techniques.animation-ripper]] — 이 하네스가 비교할 대상(트랜지션 지문)을 만드는 앞 단계
- [[techniques.adversarial-verification]] — 원리적으로 가장 가까운 기존 검증 기법(notion에서 실증됨, 단 정적 DOM 한정)
