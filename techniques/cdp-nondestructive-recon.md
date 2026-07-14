---
id: techniques.cdp-nondestructive-recon
title: CDP 비파괴 정찰 (peek 패턴, 리로드 금지)
doctype: technique
status: standard
proven_in: [canvas, notion, akiflow]
related: [techniques.cdp-raw-driver, techniques.dom-first-measurement, techniques.port-profile-isolation, techniques.url-escape-guard]
evidence:
  - "clone-campaign-kit/harness/peek.py — 'shot/dom/tokens/probe/click' 서브커맨드, 리로드 없이 attach만"
  - "260622_notion-clone/harness/peek.py 독스트링 — '실제 Notion 웹에 ATTACH(리로드 금지)'"
  - "260615_canvas-clone/harness/rip_dump.py, rip_crawl.py — 노드 개수 floor invariant 복원, PROTECTED_NODE_SELECTORS"
  - "260622_akiflow-clone — peek.py(실물, read-only attach) / cap.py(클론) 분리 harness"
updated: 2026-07-14
owner: 박춘순
---

# CDP 비파괴 정찰 (peek 패턴, 리로드 금지)

**한 줄**: 실물 앱 세션은 절대 리로드하지 않고 CDP로 attach만 해서 훔쳐본다("peek"). 클릭 등 상태 변경 액션을 할 때도 끝나면 원상복구한다.

## 언제 쓰나
실물 서비스(회사 계정 로그인 상태, 실제 데이터가 담긴 세션)를 정찰할 때 항상. 리로드하면 로그인 세션이 날아가거나, 실제 사용자 데이터/과금이 걸린 작업(예: 실제 GENERATE 호출)이 유발될 수 있다.

## 3캠페인 공통 패턴
- **notion** `harness/peek.py`: `shot <label>`(스크린샷), `dom <label>`(DOM 덤프), `tokens`(디자인 토큰), `probe`(컨트롤 인벤토리), `click "<sel>" <label>`(클릭 후 캡처 — 비파괴). RIP-PIPELINE.md 명문 규칙: "실물=스크래치 존 외 read-only·bringToFront 금지."
- **canvas** `rip_dump.py`/`rip_crawl.py`: 매 세션 끝에 "비파괴 원칙 준수" 로그 — 실물 샌드박스가 항상 원래 노드 개수(예: 2개)로 끝나도록 강제 복원. `PROTECTED_NODE_SELECTORS`로 진짜 결과 노드는 크롤러가 절대 못 건드리게 차단.
- **akiflow**: `peek.py`(실물, read-only) / `cap.py`(클론, 자유롭게 조작) 로 아예 스크립트 레벨에서 권한을 분리.
- **clone-campaign-kit** `harness/peek.py`: 3캠페인에서 검증된 걸 범용 도구로 승격한 버전.

## 왜 필요한가
- 리로드/네비게이션은 세션 상태를 깨뜨림 (예: canvas에서 로고 클릭이 실수로 `higgsfield.ai/asset/all`로 네비게이션 — → [[techniques.url-escape-guard]]로 방어).
- 실물에 GENERATE 같은 과금 액션을 실수로 트리거하면 실제 비용 발생. 정찰은 절대 그런 액션을 유발하면 안 됨.

## 함정
- "read-only"라고 클릭 자체를 금지하는 게 아니다 — 클릭해서 상태를 보되(hover/열기 등), 끝나면 반드시 원상복구(닫기/취소)까지가 한 세트.
- 크롤러처럼 대량 자동 클릭을 돌릴 때는 노드/상태 개수 invariant를 코드로 강제해야 사람이 매번 확인 안 해도 안전하다.

## 함정 (2026-07-14 notion 실전 추가)
- **비파괴 도그마**: "리로드 금지·비파괴"가 "조작 금지"로 과잉 확대되면 지연마운트 UI(호버 툴바·팝오버) 실측을 포기하게 되고, 그 공백을 워커가 자작 자산으로 메꾼다(notion 아이콘 자작 사고). 파괴 허용 존(오너가 개방한 워크스페이스)에서는 **hover/click 조작 실측이 기본 절차** — "실측 불가" 선언 전에 ①기술적으로 불가한가 ②정책상 불가한가 ③정책이 최신 오너 지시와 일치하는가를 순서대로 확인. 낡은 read-only 조항이 문서에 잔존하면 오너 해제 지시보다 우선 적용되는 사고가 난다 — 개방 지시는 받는 즉시 모든 관련 문서의 잔존 조항을 소거할 것.

## 관련
- [[techniques.cdp-raw-driver]] — attach 자체가 hang되는 문제(좀비 탭)를 우회하는 하위 기법
- [[techniques.url-escape-guard]] — 정찰 중 실수 네비게이션 방어
