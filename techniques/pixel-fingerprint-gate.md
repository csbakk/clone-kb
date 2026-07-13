---
id: techniques.pixel-fingerprint-gate
title: 픽셀 지문 게이트 (≥99% 점수 재현성)
doctype: technique
status: experimental
proven_in: []
related: [techniques.dom-first-measurement, techniques.pixel-screenshot-as-primary-oracle, pipelines.99-percent]
evidence:
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md §4, §6 — 판정식 항목⑤(픽셀 지문 ≥99%), 파일럿 기준 '≥99% 점수 재현성(2회 연속 ±0.1%)', P4 로드맵, 2026-07-13 기준 미착수"
updated: 2026-07-13
owner: 박춘순
---

# 픽셀 지문 게이트 (≥99% 점수 재현성)

**한 줄**: DOM diff가 0이어도 "육안으로 봤을 때 진짜 똑같아 보이는가"는 별개 문제다. 최종 확인 레이어로 픽셀 비교 점수를 다시 쓰되, [[techniques.pixel-screenshot-as-primary-oracle]]처럼 1차 오라클로 쓰는 게 아니라 **마지막 게이트 하나로만** 좁혀 쓰려는 개념.

## 상태: P4 로드맵, 미착수
승격 기준: "≥99% 점수 재현성(2회 연속 ±0.1%)" — 즉 같은 비교를 두 번 돌려도 점수가 흔들리지 않아야 신뢰 가능하다는 전제까지 명시되어 있음. 2026-07-13 기준 스크립트·실행 기록 없음.

## pixel-screenshot-as-primary-oracle과의 관계 (중요한 구분)
이 기법은 "픽셀 비교를 되살리자"는 게 아니라, DOM/RIP 파이프라인으로 구조적 델타를 0에 가깝게 만든 **이후**, 폰트 렌더링·서브픽셀처럼 DOM으로는 못 잡는 최후의 잔차만 픽셀로 재확인하자는 것. 1차 오라클 자리는 여전히 [[techniques.dom-first-measurement]]가 차지한다.

## 관련
- [[techniques.pixel-screenshot-as-primary-oracle]] — 이 기법과 혼동하면 안 되는 은퇴한 구방식(1차 오라클로서의 픽셀 비교)
