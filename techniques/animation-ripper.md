---
id: techniques.animation-ripper
title: 애니메이션 리퍼 (트랜지션 지문 일치)
doctype: technique
status: experimental
proven_in: []
related: [techniques.dom-first-measurement, techniques.twin-mirror-harness, pipelines.99-percent]
evidence:
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md §4, §5 — 판정식 항목②(동작 델타 0), P3 로드맵('애니메이션 리퍼 → 트윈미러 하네스'), 2026-07-13 기준 미착수"
updated: 2026-07-13
owner: 박춘순
---

# 애니메이션 리퍼 (트랜지션 지문 일치)

**한 줄**: [[techniques.dom-first-measurement]]가 명시적으로 인정하는 약점 — "AI는 영상을 못 본다, 연속 스텝 스크린샷만 본다" — 을 메우기 위한 계획. 트랜지션(easing, duration, keyframe)을 실물·클론에서 각각 "지문"으로 뽑아 비교하려는 개념.

## 상태: P3 로드맵, 미착수
canvas 99% 로드맵에서 P1(cross-paste)·P2(explorer 승격) 다음 단계로 예정된 항목. 2026-07-13 기준 스크립트도 파일럿 실행도 없음 — 판정식 항목②("동작 델타 0")의 자리만 예약되어 있는 상태.

## 왜 필요한가 (예상 근거)
정적 스타일(색상/크기/위치)은 DOM computedStyle로 완벽히 잡히지만, transition-duration/easing-function/keyframe 시퀀스 같은 **시간축 속성**은 순간 스냅샷으로는 못 잡는다. [[techniques.record-during-hover]]가 이산적 상태변화(add/remove/attr)는 잡지만 연속적인 보간(interpolation) 곡선 자체는 별도 캡처가 필요.

## 관련
- [[techniques.twin-mirror-harness]] — 같은 로드맵 단계에서 이어지는 다음 개념(실물·클론을 나란히 재생해 비교)
