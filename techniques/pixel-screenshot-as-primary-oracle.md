---
id: techniques.pixel-screenshot-as-primary-oracle
title: 픽셀 스크린샷을 1차 오라클로 (은퇴)
doctype: technique
status: retired
superseded_by: techniques.dom-first-measurement
proven_in: []
related: [techniques.dom-first-measurement, techniques.pixel-fingerprint-gate]
evidence:
  - "260622_notion-clone/CLONE-METHOD.md — '★측정은 DOM 기반으로 (픽셀 스샷 대체 — 2026-07-10 채택, 모든 웹 클론 재사용)'"
  - "260615_canvas-clone/docs/2026-07-11-parity-campaign-strategy.md §4 — '픽셀 스샷 대신 DOM(2026-07-10 채택) — 추측 0'"
  - "clone-campaign-kit/NIGHT-RUN.md — 완전 폐기는 아님: 연속 스텝 동작(애니메이션) 캡처용으로는 스크린샷이 여전히 '★기본'('AI는 영상 재생 불가·프레임만 봄 → 연속 스텝 screenshot이 영상보다 낫다')"
updated: 2026-07-13
owner: 박춘순
---

# 픽셀 스크린샷을 1차 오라클로 (은퇴)

**한 줄**: 실물 vs 클론 대조의 1차 수치 오라클을 픽셀 스크린샷 diff로 삼던 방식. **2026-07-10, canvas·notion 두 캠페인이 같은 날 독립적으로 폐기 결정** — 후속: [[techniques.dom-first-measurement]].

## 왜 은퇴했나
- retina 스케일 드리프트·서브픽셀 렌더링에 취약해 오탐이 잦았다.
- "어디가 왜 다른지"를 알려주지 않는다 — 픽셀 diff는 좌표만 주지 원인 속성(border-radius 값이 다른지, color가 다른지)을 안 준다.
- DOM/computedStyle 기반 측정이 같은 문제를 더 정확하고 더 설명 가능하게 푼다는 게 두 캠페인에서 각각 실증됨.

## 완전 폐기는 아니다 (뉘앙스 — 정직하게 기록)
clone-campaign-kit NIGHT-RUN.md는 "AI가 영상을 재생할 수 없고 프레임만 볼 수 있으므로, 연속 스텝 스크린샷이 동영상보다 낫다"며 **동작(애니메이션) 캡처 용도로는 스크린샷을 여전히 기본으로 쓴다**고 명시한다. 은퇴한 것은 "정적 UI 상태를 수치로 비교하는 1차 오라클" 역할이지, 스크린샷이라는 수단 자체가 아니다. → [[techniques.animation-ripper]](experimental)가 이 남은 용도를 체계화하려는 후속 시도.

## 관련
- [[techniques.dom-first-measurement]] — 이 기법을 대체한 standard 기법
- [[techniques.pixel-fingerprint-gate]] — 픽셀 비교를 "최후의 보조 게이트"로만 좁혀 되살리려는 별개의 experimental 시도(1차 오라클 자리를 다시 차지하려는 게 아님)
