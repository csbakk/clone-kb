---
id: techniques.clipboard-format-interop
title: 클립보드 포맷 상호운용 — 복사/붙여넣기로 원본과 서식 왕복
doctype: technique
status: experimental
proven_in: []
related: [techniques.structure-first-cloning, techniques.dom-first-measurement]
updated: 2026-07-19
owner: 박춘순
---

# 클립보드 포맷 상호운용 (Clipboard Format Interop)

**한 줄**: 클론과 원본 앱 사이에서 **복사→붙여넣기 시 서식·구조가 유지**되게 하려면, 원본이 클립보드에 payload를 **어떤 저장소·어떤 포맷**으로 넣는지 규명하고 클론이 그 포맷을 **읽고 쓰게** 한다. 별도 "○○로 복사" 버튼 없이 일반 복사에 투명 통합.

## 왜

클론이 아무리 화면이 똑같아도, 복사한 콘텐츠를 원본 앱에 붙여넣었을 때 평문으로 풀려버리면 "진짜 상호운용"이 아니다. 반대로 원본→클론 붙여넣기가 구조를 살리면 데이터 이식·마이그레이션이 공짜로 따라온다. 클립보드는 **앱 간 계약**이라, 그 계약 포맷만 맞추면 양방향이 열린다.

## 1. 먼저 규명 — payload가 어디 사는가 (2패턴)

복사 전후로 4경로를 실측한다: **클립보드 커스텀 MIME · localStorage · sessionStorage · IndexedDB**.

- **패턴 A — localStorage 마커**(예: Higgsfield Canvas): 실제 payload를 `localStorage['<app>-clipboard']`에 통째로 넣고 OS 클립보드엔 마커(uuid)만. → `localStorage.getItem('...')` 한 줄로 전체 구조 추출.
- **패턴 B — 클립보드 커스텀 MIME**(예: Notion): payload를 `text/_<app>-blocks-...` 같은 **커스텀 MIME**에 담아 OS 클립보드에 넣음(협업·크로스탭 붙여넣기 목적). localStorage/IndexedDB는 무변화. → **trusted OS paste 이벤트의 `e.clipboardData.getData('<mime>')`로만** 읽힘(Chrome async `clipboard.read()`는 커스텀 타입 미노출).

규명법: 스크래치에서 실제(trusted, osascript) Cmd+C → localStorage/sessionStorage 키 diff + paste 이벤트 `clipboardData.types` 전수 덤프 + `indexedDB.databases()`. **실키(osascript pbcopy+Cmd+V)로 검증** — Playwright 합성 키는 OS 클립보드를 못 채워 "비었음"으로 오판한다.

## 2. 클론에 read/write 붙이기

- **쓰기(클론→원본)**: copy 이벤트 가로채 `e.clipboardData.setData('<mime>', json)` — `setData`는 임의 MIME 허용, 기술 장벽 없음. **여러 포맷 동시**로: 원본 커스텀 MIME(최우선) + `text/html`(범용 폴백) + `text/plain`(최종 폴백).
- **읽기(원본→클론)**: paste 이벤트에서 커스텀 MIME 있으면 파싱→클론 모델 역변환, 없으면 html→plain 폴백.
- **★버튼 만들지 마라 — 일반 복사에 투명 통합**: 원본 앱도 복사 한 번에 다중 포맷을 동시에 넣는다. 별도 "○○로 복사" 버튼은 원본과 다른 UX가 되고 인지부하를 만든다. 붙여넣는 앱이 자기가 읽을 최상위 포맷을 고르게 두면 된다.

## 3. 재사용 — 스키마 변환기

클론이 이미 **API 파리티**([[techniques.structure-first-cloning]] §전층지도 ⑦)를 구현했다면 클론모델↔원본스키마 **양방향 변환기가 이미 있다** — 그 직렬화/역직렬화를 클립보드 어댑터로 재사용한다. 새로 만들 건 클립보드 read/write 껍데기뿐. (notion: `harness/notion_api_server.py` 변환기 재사용 예정)

## 4. 리스크

- **스키마 정확도**: 원본 내부 스키마(id 형식·rich-text annotations·content 배열)를 정확히 생성해야 원본이 필드를 안 버린다.
- **세션 의존 필드**(최대 미지수): `space_id`·workspace·버전 필드를 원본이 붙여넣기 때 검증하면 "외부 출처"로 보고 거부/무시할 수 있다 → **PoC 실측 필수**.
- **왕복 손실**: 특수 블록(synced·DB view 등)은 완전 왕복 어려움 → 지원 타입 명시 + 폴백.
- **trusted 입력**: 커스텀 MIME는 실제 OS copy/paste에서만. 자동화 테스트는 osascript trusted 경로.

## 5. 절차

1. payload 위치 규명(§1, 4경로 실측).
2. **PoC 먼저** — 가장 큰 미지수(세션 의존 필드)를 스크래치 왕복으로 실측. 통과 전엔 구현 확대 금지.
3. 핵심 타입부터 read/write 붙이고 회귀 게이트(왕복 무손실 diff) + 시각 증거(양방향 캡처).

## 실증 대기

- **notion(설계 완료, PoC 대기, 2026-07-19)**: 커스텀 MIME `text/_notion-blocks-v3-production` 규명(패턴 B). 설계 `260622_notion-clone/ref/design/CLIPBOARD-PARITY.md`, 조사 `ref/rip/notion_clipboard_investigation.md`. PoC 통과 시 verified 승격 후보.
- **canvas(참고, 패턴 A)**: Higgsfield Canvas localStorage 마커 방식 — [[canvas-clone-parity-campaign]] 클립보드 recon에서 확인.
