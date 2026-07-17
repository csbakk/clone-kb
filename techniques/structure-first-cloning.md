---
id: techniques.structure-first-cloning
title: 구조-우선 클론 (골격→스타일→동작 순서 원칙)
doctype: technique
status: standard
proven_in: [notion, canvas]
related: [techniques.measured-css-porting, techniques.pixel-diff-baseline, techniques.rip-repair-loop, techniques.dom-first-measurement]
evidence:
  - "notion 수렴 루프(2026-07-17)의 갭 대부분이 구조 기원으로 판명: 행높이 1px=tr 보더 레이어·거터 96px 이중예약·제목 잘림=input vs h1·번호목록 깨짐=마커/텍스트 부모 분리 — 골격이 같았으면 없었을 갭들"
  - "오너 DevTools 요소 인스펙션(제목 720×48/0px8px/textbox vs 클론 720×56/4px0/heading)이 픽셀 96% 아래의 골격 불일치 층을 드러냄"
  - "canvas 세션21(2026-07-17) — **retrofit 시나리오 첫 실증**: 이미 스타일-먼저로 진행돼온 canvas 캠페인에 원칙을 소급 적용. 헤더 타이틀 span래퍼 1줄 수정이 6상태 속성diff 7295→4364(-40%) 동반 감소, 라이트박스 메타패널 신설이 2374→1696(-29%) 동반 감소 — 구조 정합 1건이 스타일 레이어 다수를 공짜로 데려오는 notion과 동일 메커니즘이 별개 앱·별개 프레임워크(@xyflow 노드캔버스)에서도 재현됨"
  - "canvas 세션21 — 프롬프트 입력 골격(렌더러 심장부급, 전 Generate 노드 공통 textarea→contentEditable)을 image→video→llm→audio→promptnode→inspector 6개 소비처에 순차 확산, 매 라운드 이전 타입 전체 무회귀 재확인(18/18×6회)으로 완결. 이미 프로덕션 검증된 contentEditable 패턴(TextNode/StickyNoteNode의 useEditableSeed) 재사용이 골격 리팩터의 신규 리스크를 낮춘 사례 — 골격 교체가 '렌더러 심장부'라도 기존 검증 패턴 재사용 시 점진 확산 가능함을 실증"
updated: 2026-07-17
owner: 박춘순
---

# 구조-우선 클론 (Structure-First)

**한 줄**: 클론의 복사 순서는 **①골격(DOM 구조) → ②스타일(computed) → ③동작(이벤트·JS)** — 골격을 먼저 복사해야 스타일이 1:1 이식되고 픽셀이 "보정 없이" 맞는다. **오너 직접 채택 원칙(2026-07-17), 모든 클론 캠페인의 1순위.**

## 왜 (notion 캠페인 실증)

스타일-먼저(값 포팅)로 가면 **보정 스택**이 생긴다: 요소 A의 8px 차이를 요소 B의 마진으로 상쇄 → 특정 상태에선 픽셀이 맞지만 내용이 바뀌면 깨진다(번호목록: 마커와 텍스트가 다른 부모라 높이 어긋남). 수렴 루프 이터레이션 7회의 갭 대부분이 구조 기원이었다 — 골격이 같았으면 스타일 단계가 거의 공짜였다.

## 순서 원칙

1. **골격**: 블록/컴포넌트 단위로 실물의 DOM 스켈레톤을 채택 — 태그(h1 vs input), a11y role(textbox vs heading), **부모-자식 그룹핑**(마커+텍스트 단일 부모), 래퍼 체인, contenteditable 배치. 실물 스켈레톤 자동 추출(태그·role·padding·그룹핑 덤프) → 클론 렌더러가 같은 골격을 뱉게 → **구조 게이트**로 동치 고정.
2. **스타일**: 골격이 같으면 computed 값·셀렉터 규칙을 거의 그대로 이식([[techniques.measured-css-porting]]) — 보정 불필요.
3. **동작**: 이벤트·키보드·상태 전이·JS 로직 복사/재현. 검증은 [[techniques.pixel-diff-baseline]](픽셀)+구조 게이트(골격)+기능 게이트(동작) 3축.

→ **복사 가능한 것을 전부 복사하면 가시·상호작용 층은 99% 도달 가능.** 잔여 1% = 복사 불가능물(서버 로직·외부 iframe 콘텐츠·백엔드 데이터)로, 재구현 대상.

## 함정

- 스타일부터 시작하면 수렴은 되지만(픽셀 91→96%) 요소 인스펙션 층에서 불일치가 남고, 갭 수복이 "두더지잡기"가 된다 — notion에서 7이터레이션 지불하고 배운 것.
- 골격 리팩터는 렌더러 심장부를 건드림 — 반드시 게이트망([[techniques.regression-harness-suite]]) 선행 + 블록 타입 단위로 점진.
- 이미 스타일-먼저로 진행된 캠페인은 골격을 **retrofit**(블록 단위 골격 교체, 픽셀 기준선으로 무회귀 확인)한다.

## 실증 2 — canvas retrofit (2026-07-17, 세션21)

notion은 처음부터 구조-우선으로 설계된 캠페인이었지만, canvas는 세션1~20을 스타일-먼저(값 포팅) 방식으로 누적 진행해온 캠페인이다 — 위 §함정의 "이미 스타일-먼저로 진행된 캠페인" 시나리오를 실제로 만난 첫 사례. 소급 절차:

1. **정찰 우선, 신규 캡처 없이**: 기존 RIP 델타(19상태) + 서술형 RECON 문서 + 현재 소스코드(git log/grep) 3축 교차검증만으로 확정 갭 3건(헤더 span래퍼·라이트박스 메타패널·프롬프트 골격)을 추려냄. 델타 문서의 스테일 항목(이미 다른 커밋으로 해결된 5건)과 캡처 아티팩트(소스가 이미 자인한 하네스 오탐)를 먼저 걸러낸 뒤에만 "진짜 구조 갭"으로 확정 — 신규 실측 없이 기존 산출물 재해석만으로 우선순위를 세울 수 있음을 보임.
2. **블록 단위 점진 리트로핏**: 헤더span(1줄, 3곳) → 라이트박스 메타패널(신규 섹션 추가, 기존 구조 안건드림) → 프롬프트 골격(렌더러 심장부, 6개 소비처 순차 확산) 순으로 리스크가 낮은 것부터. 매 블록마다 RIP isolated resweep으로 무회귀 확인 후 다음 블록 진행.
3. **결과**: 헤더span 1건이 6상태 diff -40%, 라이트박스 1건이 -29% 동반 감소 — notion과 동일하게 "구조 정합이 스타일 레이어를 공짜로 데려온다"는 메커니즘이 재현됨. 프롬프트 골격은 이미 프로덕션 검증된 contentEditable 패턴(다른 노드 타입의 `useEditableSeed`)을 재사용해 렌더러 심장부급 리팩터도 신규 리스크 없이 6타입 확산 가능함을 보임(매 라운드 이전 타입 전체 무회귀 재확인 18/18×6회).

→ retrofit이 스타일-먼저 캠페인에도 유효한 탈출 경로임을 확인. 상세: `clone-kb/runs/2026-07-17-canvas-structfirst.md`, canvas repo `ref/_STRUCTURE_FIRST_ROADMAP.md`.
