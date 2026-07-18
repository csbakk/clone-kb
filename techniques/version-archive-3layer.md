---
id: techniques.version-archive-3layer
title: 버전-증명 3층 아카이브 (MHTML + PNG + localStorage)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.webgl-node-rendering-clone, techniques.canvas-clipboard-localstorage, techniques.baseline-then-diff, techniques.rip-css-dump]
evidence:
  - "260615_canvas-clone ref/real-recapture-2026-07-18/_ARCHIVE-METHOD.md (2026-07-18) — 3층 박제 표: DOM UI(셸·툴바·인스펙터·피커·메뉴·모달)=MHTML(`Page.captureSnapshot {format:mhtml}`)+outerHTML, WebGL 노드=컴포지터 레벨 스크린샷 PNG, 노드 구조/데이터=localStorage 복사(Select-All+Copy). `<canvas>`는 MHTML에 빈 태그로만 담기고(그림=GPU 비트맵, 직렬화 안 됨), `canvas.toDataURL()`은 `preserveDrawingBuffer:true` 없이는 빈 이미지라 컴포지터 스크린샷이 유일한 확실한 방법임을 명문화"
  - "260615_canvas-clone harness/real_archive.py (2026-07-18) — 위 3층을 자동화한 스크립트: `cdp.send('Page.captureSnapshot', {format:'mhtml'})` + `document.documentElement.outerHTML` + `pg.screenshot()` + 캔버스별 `localStorage.getItem('higgsfield-canvas-clipboard')` 순차 저장, 캐던스=월 1회(`OUT = .../dom-archive/<YYYY-MM>/`)"
  - "260615_canvas-clone ref/real-recapture-2026-07-18/_MANIFEST.md (2026-07-18) — 버전 정책 표: 구버전(업그레이드 이전) 캡처는 git 태그 `baseline-pre-upgrade-2026-07-18`+기존 ref/ 폴더로 절대 덮어쓰기 금지 보존, 신버전은 이 폴더에만 신규 캡처 — OLD vs UPDATED 대조로 '업그레이드로 달라진 UI'를 드리프트 검출"
updated: 2026-07-18
owner: 박춘순
---

# 버전-증명 3층 아카이브 (MHTML + PNG + localStorage)

**한 줄**: 클론 대상이 언제든 업그레이드/드리프트할 수 있는 살아있는 앱일 때, 월 단위로 **MHTML(DOM 전체)** + **PNG 스크린샷(WebGL/캔버스 픽셀)** + **localStorage/클립보드 JSON(데이터모델)** 3층을 겹쳐 박제하면 어느 한 층이 못 담는 것을 다른 층이 메꿔 아무것도 잃지 않는다.

## 왜 3층인가 — 각 층이 무엇을 담고 무엇을 놓치나
| 층 | 방법 | 담기는 것 | 안 담기는 것 |
|---|---|---|---|
| **DOM UI** (셸·툴바·인스펙터·피커·메뉴·모달) | MHTML(CDP `Page.captureSnapshot {format:mhtml}`) + outerHTML | 골격·계층·클래스·computed·리소스(CSS·이미지 인라인) — 나중에 그냥 열면 보임 | 동작(JS), WebGL 노드(빈 태그) |
| **WebGL/캔버스 노드** | PNG 스크린샷(컴포지터 레벨) | 시각(픽셀) | 노드 DOM(애초에 없음, [[techniques.webgl-node-rendering-clone]]) |
| **노드 구조/데이터모델** | localStorage/클립보드 복사(Select-All+Copy → JSON) | 타입·파라미터·결과·썸네일 — 구조를 데이터로 | 시각적 배치의 "느낌"(좌표는 있지만 렌더 결과는 아님) |

**핵심 함정 2가지**: ①`<canvas>`는 MHTML에 **빈 태그**로만 담긴다(그림은 GPU 비트맵이라 직렬화 자체가 안 됨) → 노드 시각은 반드시 PNG로 별도 확보. ②WebGL `canvas.toDataURL()`은 `preserveDrawingBuffer:true`가 아니면 빈 이미지를 반환 → 컴포지터(화면 합성 결과) 스크린샷이 유일하게 확실한 방법.

## 캐던스와 버전 정책
- **월 1회** 스냅샷(`dom-archive/<YYYY-MM>/`). 목적은 "언제든 이 시점의 구조를 열어볼 수 있게" — 실시간 미러가 아니라 정지된 사진첩.
- **구버전은 덮어쓰지 않는다** — 업그레이드가 감지되면 그 시점을 git 태그(예: `baseline-pre-upgrade-<날짜>`)로 고정하고, 기존 캡처 폴더는 무수정 보존. 새 캡처는 새 날짜 폴더에만 쓴다.
- OLD vs UPDATED를 대조하면 "업그레이드로 실제로 달라진 것"만 드리프트로 추려낼 수 있다 — [[techniques.baseline-then-diff]]의 diff-only 운영이 여기서 시작된다.

## 캡처 대상 (매 회차 공통 세트)
1. 셸 기본 상태(로드 완료, fit-view) — MHTML+outerHTML+PNG.
2. 노드 타입별 인스펙터 열림 상태(각 타입 클릭 → 우측 패널) — DOM이므로 MHTML+PNG.
3. 피커/드롭다운 열림 상태(모델·비율·해상도·duration 등) — 각각 MHTML+PNG.
4. 메뉴/모달(캔버스 우클릭·Add-node·폴더 생성 등) — 각각 MHTML+PNG.
5. 대표 캔버스(구조 다양성 커버) 여러 개의 localStorage 데이터모델 JSON.

## 로그인 의존성
아카이브는 로그인된 세션이 필수 — 전용 CDP 프로필(예: 별도 `--user-data-dir`)에 쿠키가 유지되면 무인/월간 실행이 재로그인 없이 돈다. 세션 만료 시엔 "로그인 필요" 통지만 하고 사람이 그 창에 로그인 후 재실행(우아한 skip, [[techniques.night-run-sop]] 원칙과 동일).

## 판단 규율 — 무엇을 클론에 반영하고 무엇을 아카이브만 하나
- **기능/구조 변화**(새 노드타입·모델·파라미터·인스펙터 컨트롤) → 클론에 반영(DOM/JSON으로 캡처 가능한 것들).
- **순수 시각 리스타일**(WebGL 노드 픽셀 룩 변화 등) → **아카이브만**, 픽셀 재스킨은 쫓지 않는다(러닝머신 방지).
- 판단 기준 한 줄: "이 변화가 방법론/엔진베이스에 기여하나?" 예 → 반영, 아니오 → 아카이브. 이 규율의 상위 원칙은 [[techniques.baseline-then-diff]].

## 관련
- [[techniques.webgl-node-rendering-clone]] — 이 3층 아카이브가 필요해진 직접 계기(노드가 WebGL이라 DOM 단독 캡처로는 불충분)
- [[techniques.canvas-clipboard-localstorage]] — 3층 중 데이터모델 층의 구체 메커니즘
- [[techniques.baseline-then-diff]] — 이 아카이브를 "한 번 전수 + 이후 diff-only"로 운영하는 상위 관리 원칙
- [[techniques.rip-css-dump]] — DOM 층 전수 덤프의 자매 기법(RIP은 클론 대조용, 이 카드는 버전 보존용)
