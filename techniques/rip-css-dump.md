---
id: techniques.rip-css-dump
title: RIP 레이어① CSS/DOM 전수 덤프
doctype: technique
status: standard
proven_in: [canvas, notion]
related: [techniques.rip-crawler, techniques.rip-repair-loop, techniques.dom-first-measurement, techniques.cdp-raw-driver, pipelines.rip-v1]
evidence:
  - "260615_canvas-clone/harness/rip_dump.py + rip_align.py — cdp_raw 기반, 좀비탭 우회, canvasSpace 좌표 정규화, 19/19 상태 전수 덤프"
  - "260615_canvas-clone/ref/_RIP_MASTER_DELTA.md — attribute-diff 38,476→30,580(-20.5%), --radius-btn(99px) vs --radius-pill(999px) 토큰 분리 사례"
  - "260622_notion-clone/ref/전수-리핑-파이프라인.md·RIP-PIPELINE.md — 10개 상태 테스트, 캘린더 뷰 구조 델타 157→18(-88.5%), title_hover 29→0"
updated: 2026-07-13
owner: 박춘순
---

# RIP 레이어① CSS/DOM 전수 덤프

**한 줄**: "아는 것만 체크리스트로 재는" 방식을 버리고, 지정한 UI 상태의 서브트리 전체(모든 엘리먼트 × 약 68개 CSS 속성 + bbox + role/aria + SVG)를 실물·클론 양쪽에서 덤프해 기계가 델타를 자동 발견하게 한다. **canvas와 notion 두 캠페인에서 각각 독립 실증되어 standard로 승격.**

## 왜 (근본 이유)
체크리스트 기반 실측은 "사람이 열거한 항목"만 잡는다. 실제로 notion 세션에서 체크리스트가 놓친 걸 사람 눈이 우연히 잡은 사례가 반복되자, "전수(全數)로 뜯어서 기계가 델타를 찾게 하자"는 방향 전환이 나왔다(전수-리핑-파이프라인.md).

## 어떻게
1. 상태를 URL + 도달 클릭 시퀀스로 JSON 명세 (→ [[techniques.state-spec-json]]).
2. 같은 스크립트(`rip_dump.py`)를 실물/클론 양쪽에 그대로 실행 — 상태 스펙만 다르게.
3. 클래스명에 의존하지 않는 자동 정렬(class-agnostic auto-matching)로 실물 엘리먼트와 클론 엘리먼트를 짝짓는다.
4. `rip_align.py`가 짝지어진 엘리먼트 간 속성 diff를 계산 — 매칭 안 된 엘리먼트는 "구조적 델타"로 별도 집계.
5. 노드캔버스 앱은 좌표계가 `translate(tx,ty) scale(z)`로 변환되어 있으므로 flow-space(zoom=1 기준)로 정규화 후 비교 (`canvasSpace: true/false` 플래그).

## 실측 결과 (근거)
- **canvas**: 19개 상태 전수 덤프, 0 스킵. attribute-diff 38,476 → 30,580(-20.5%, 글로벌 CSS 리셋 배치 1회 이후). 1차 시도 과잉교정 사례: `999px→99px` 일괄 치환이 `.hf-toolbar`(진짜 999px)를 깨뜨려 `--radius-btn`(99px)/`--radius-pill`(999px) 토큰을 분리해야 했음 — 전수 덤프가 아니었으면 이 미묘한 예외를 놓쳤을 것.
- **notion**: 10개 상태에서 구조 델타 1539→1083(-30%), 캘린더 뷰 157→18(**-88.5%**, 최대폭), title_hover 29→**0**(완전 수렴). 기계가 사람이 못 잡은 것들(SVG 찌그러짐의 근본원인=UA 버튼 패딩, 코멘트 첨부/멘션 버튼 누락, "아이콘 추가=피커 없이 즉시 랜덤 배정" 동작, 셀렉터 off-by-one 버그 등)을 자동 발견.

## 함정
- CDP `connect_over_cdp()`가 좀비 탭 때문에 180초 행업되는 문제 — `rip_dump.py`는 이를 우회하기 위해 별도의 [[techniques.cdp-raw-driver]]를 사용한다.
- 델타를 0으로 만들려는 과잉교정은 다른 곳을 깨뜨릴 수 있다 — 반드시 재덤프로 재검증(→ [[techniques.rip-repair-loop]]).

## 관련
- [[pipelines.rip-v1]] — 이 레이어를 포함한 3단계 RIP 파이프라인 전체
