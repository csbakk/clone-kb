---
id: techniques.dom-first-measurement
title: DOM 기반 측정 (픽셀 스샷 대체)
doctype: technique
status: standard
proven_in: [canvas, notion]
related: [techniques.cdp-nondestructive-recon, techniques.rip-css-dump, techniques.pixel-screenshot-as-primary-oracle, techniques.record-during-hover]
evidence:
  - "260615_canvas-clone/harness/dom_snap.py — DOM 인벤토리(box+computedStyle) + 스샷은 육안검증 보조로만"
  - "260615_canvas-clone/docs/2026-07-11-parity-campaign-strategy.md §4 — '픽셀 스샷 대신 DOM(2026-07-10 채택) — 추측 0'"
  - "260622_notion-clone/CLONE-METHOD.md 헤더 — '★측정은 DOM 기반으로 (픽셀 스샷 대체 — 2026-07-10 채택, 모든 웹 클론 재사용)'"
  - "260622_notion-clone/harness/dom_recorder.py 헤더 — '왜: 픽셀 측정은 부정확·retina 드리프트에 취약'"
updated: 2026-07-13
owner: 박춘순
---

# DOM 기반 측정 (픽셀 스샷 대체)

**한 줄**: 실물 vs 클론을 대조할 때 픽셀 스크린샷을 1차 오라클로 쓰지 않는다. DOM 트리 + `getComputedStyle` 값을 기계로 diff한다. 스샷은 육안 보조로만 남긴다.

## 언제 쓰나
클론 캠페인의 모든 "갭 측정" 단계 기본값. 새 캠페인을 시작할 때 harness를 처음 짤 때부터 이 원칙을 깔고 간다.

## 왜 (근본 이유)
- 픽셀 스크린샷은 retina 스케일 드리프트·서브픽셀 렌더링에 취약해 "달라 보이는데 사실 같음/같아 보이는데 사실 다름" 오탐이 잦다.
- 스크린샷 diff는 "어디가 왜 다른지"를 알려주지 않는다. DOM/computedStyle diff는 속성명·값까지 바로 나온다 (예: `borderRadius: 99px vs 999px`).
- 2026-07-10에 canvas·notion 두 캠페인이 **같은 날 독립적으로** 이 원칙을 채택 — 우연이 아니라 픽셀 비교의 한계를 반복 경험한 결과.

## 어떻게
- **canvas**: `harness/dom_snap.py` — Playwright `connect_over_cdp`로 어태치, 대상 subtree의 box+computedStyle(color/bg/border/radius/font/shadow/backdrop/opacity)을 최대 600 엘리먼트까지 덤프 → `{label}.json` + `{label}.png`(육안 보조). `python3 dom_snap.py <url_substr> <label>`.
- **notion**: `harness/dom_recorder.py` — 정적 UI는 `snapshot <selector>`(엘리먼트 트리 워크 + computedStyle), 동적 동작은 `record`→상호작용→`read`(MutationObserver 주입 후 이벤트 로그).
- 두 구현 모두 "관찰 루트를 좁게 잡아라" 원칙 공유 — notion에서 `document.body` 전체를 관찰하다 렌더러 CPU 스파이크가 난 사고(2026-07-10) 이후 `auto_stop_ms`(기본 30000ms) 자동 해제 + 좁은 root selector가 필수 규칙이 됨.

## 함정
- 관찰 루트를 너무 넓게 잡으면(예: `body` 전체 + mutation마다 `getBoundingClientRect`) CPU 스파이크 → 발열/행 걸림. 좁은 root + 개수 캡(canvas는 600개) 필수.
- 스크린샷을 완전히 버리는 게 아니다 — 연속 스텝 동작(애니메이션 프레임 등)은 AI가 영상을 못 보므로 스텝별 스크린샷이 여전히 필요(→ [[techniques.animation-ripper]] 참고). "1차 수치 오라클"에서만 제외.

## 관련
- [[techniques.pixel-screenshot-as-primary-oracle]] — 이 기법이 대체한 구방식 (retired)
- [[techniques.cdp-nondestructive-recon]] — 측정 시 실물 세션을 건드리지 않는 규율
- [[techniques.rip-css-dump]] — DOM 측정을 전수(全數) 상태로 확장한 파이프라인
