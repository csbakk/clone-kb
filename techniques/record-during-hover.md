---
id: techniques.record-during-hover
title: 호버 중 레코딩 (Clone Inspector + ci_agent)
doctype: technique
status: verified
proven_in: [notion]
related: [techniques.dom-first-measurement, techniques.adversarial-verification]
evidence:
  - "260622_notion-clone/harness/ci_agent.py — Clone Inspector 확장 구동, start()/stop()/read()/capture()"
  - "260622_notion-clone/CLONE-METHOD.md — 드래그 시 콜아웃 이동 로그(div.x78zum5 블록 제거→재삽입), 드롭라인 rgba(35,131,226,0.43), 셀렉션 halo inset:0"
  - "~/Documents/tools/clone-inspector/ (MV3 확장, v0.5.0) — MutationObserver 레코딩 + 엘리먼트 피커 + JSON export"
updated: 2026-07-13
owner: 박춘순
---

# 호버 중 레코딩 (Clone Inspector + ci_agent)

**한 줄**: hover/drag 같은 순간적 상태는 스크린샷 한 장으로 못 잡는다. 레코딩 시작 → 동작 수행 → 레코딩 정지 → DOM 변이 로그(ADD/RM/ATTR) 읽기, 이 순서로 "그 순간에 정확히 뭐가 바뀌었는지"를 잡는다.

## 원칙
"elementsFromPoint는 나타난 뒤 정확 위치에서 보조로만" — 즉 위치 스캔은 2차 확인 수단이고, **레코딩이 1차**다.

## 어떻게
- `~/Documents/tools/clone-inspector/`: MV3 Chrome 확장(v0.5.0), 툴바 토글 또는 Alt+Shift+C. 지정 root selector(기본 `body`)에 MutationObserver를 걸어 노드 추가/제거·속성/스타일 변화를 최대 8000건까지 기록.
- `harness/ci_agent.py`: CDP `pg.evaluate`로 확장을 원격 구동 — `attach()`, `ensure()`(agent.js 자동 주입), `start()`/`stop()`(레코딩), `read()`, `capture()`(computedStyle 스냅샷).
- 실제 예시(콜아웃 드래그): `div.x78zum5` 내용칸에서 블록 제거→재삽입 로그, 드롭라인 `background:rgba(35,131,226,0.43); height:4px; z-index:88`, 셀렉션 halo `inset:0; background:rgba(35,131,226,0.07); radius:4px` — 전부 정적 스크린샷으로는 절대 못 잡는 정보.

## 발열/성능 안전장치 (clone-inspector 자체 내장)
- 패널/오버레이는 shadow DOM 아래 있어 `body` 관찰이 스스로를 트리거하지 않음.
- MutationObserver 콜백 안에서 `getBoundingClientRect` 같은 강제 레이아웃 리드를 하지 않음 (레이아웃 스래싱 = "발열 원인"으로 명시).
- 레코딩 상한 8000건 + 3분 자동정지.

## 함정
- 레코딩 범위(root selector)를 너무 넓게 잡으면 [[techniques.dom-first-measurement]]에서 겪은 CPU 스파이크와 같은 문제가 재발할 수 있음 — 좁게 스코프.

## 관련
- [[techniques.dom-first-measurement]] — 같은 "픽셀 대신 DOM" 철학의 동적 버전
