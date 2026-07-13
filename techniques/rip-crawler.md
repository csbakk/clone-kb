---
id: techniques.rip-crawler
title: RIP 레이어② 인터랙션 크롤러
doctype: technique
status: verified
proven_in: [canvas, notion]
related: [techniques.rip-css-dump, techniques.rip-repair-loop, techniques.url-escape-guard, pipelines.rip-v1]
evidence:
  - "260615_canvas-clone/harness/rip_crawl.py + rip_crawl_diff.py — BLOCK_TEXT_SUBSTRINGS, PROTECTED_NODE_SELECTORS, 노드개수 floor invariant, depth-2 cap, 상태그래프 오토세이브 30스텝마다"
  - "260615_canvas-clone/ref/_RIP_CRAWL_PILOT.md — 3상태×{실물,클론}=180 후보 실행, 0 에러, 실물 네비게이션-이탈 사고 1건 포착"
  - "clone-campaign-kit/harness/rip_crawl.py — 34400B, 3캠페인 공용 도구로 승격"
updated: 2026-07-13
owner: 박춘순
---

# RIP 레이어② 인터랙션 크롤러

**한 줄**: 지정한 상태에서 상호작용 가능한 엘리먼트를 전부 자동으로 열거·실행하고, DOM 변이를 기록해 "상태 그래프"(UI상태=노드, 상호작용→결과=엣지)를 실물·클론 각각 독립적으로 만든 뒤 diff한다.

## 어떻게
- `harness/rip_crawl.py`: 각 상태에서 클릭 가능한 후보를 자동 열거 → 실행 → MutationObserver로 DOM 변이 기록 → 상태 서명(signature)으로 중복 제거 → depth-2까지 탐색.
- `rip_crawl_diff.py`: 실물 그래프 vs 클론 그래프를 diff — 같은 트리거가 다른 반응을 만드는지 자동 탐지.

## 안전장치 (비파괴 원칙과 결합)
- `BLOCK_TEXT_SUBSTRINGS`: GENERATE, Invite, Share, Delete, Undo, Duplicate, Log out 등 위험 텍스트를 가진 컨트롤은 크롤러가 절대 클릭하지 않음.
- `PROTECTED_NODE_SELECTORS`: 실물의 진짜 결과 노드는 크롤러가 못 건드림.
- 노드/상태 개수 floor invariant — 매 후보 실행 후 강제 복원.
- 타임아웃 10초/후보, 30스텝마다 그래프 오토세이브(중간에 죽어도 유실 최소화).

## 실증 결과
- **canvas pilot**: 3개 상태 × {실물,클론} = 180개 후보 실행, 에러 0. 이 과정에서 **실물 네비게이션-이탈 사고**를 실제로 잡음 — 로고 클릭이 `higgsfield.ai/asset/all`로 튕기는 걸 크롤러가 밟았고, 이게 [[techniques.url-escape-guard]] 신설의 직접 계기가 됨. 하네스 자체 버그 3건도 이 과정에서 발견·수정(뷰포트 드리프트로 인한 hover/click 오조준, 노드개수 복원이 stale 좌표에 의존하던 버그, cleanup 스킵 로직 버그).
- **notion**: RIP 파이프라인 레이어②로 편입, 레이어①의 구조 델타 축소(예: 캘린더 -88.5%)와 함께 상태 커버리지 확장에 기여.

## 함정
- 크롤러가 "다르게 반응했다"고 과잉분류하는 문제: mutation 구성이 다르지만 실제 기능은 동일하게 재현된 케이스를 구분 못 함 — notion 캠페인에서 "P3 auto-repair loop + mutation-Jaccard 분류기 정밀도"가 다음 과제로 남음(→ [[techniques.rip-repair-loop]] 참고).

## 관련
- [[techniques.url-escape-guard]] — 이 크롤러가 실제로 촉발시킨 방어 기법
