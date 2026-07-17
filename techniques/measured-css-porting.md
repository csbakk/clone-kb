---
id: techniques.measured-css-porting
title: 실측 CSS 포팅 (골격 동치 후 computed 값 그대로 이식)
doctype: technique
status: standard
proven_in: [notion, canvas]
related: [techniques.dom-first-measurement, techniques.structure-first-cloning, techniques.pixel-diff-baseline]
evidence:
  - "PLAYBOOK.md §1.3 ③스타일 포팅 — '[[techniques.dom-first-measurement]]로 실측한 computed 값을 골격이 같은 노드에 그대로 이식 (전담 카드 measured-css-porting은 아직 미작성 — 마커만 남겨둠, 다음 카드화 후보)' — 이 카드가 그 마커를 메움"
  - "ledger/2026-07.md 2026-07-17 measured-css-porting(신규 후보) — '실물 computed 실측→클론 CSS 포팅 파이프라인으로 오너 육안지적 8건+DB 3축+잔여갭 5건+풀블록 5건 전부 해소. 부산물로 가설반증 3건(컬럼순서=가나다·아웃라인=고정비율·status=그룹고정3색 — 문서/추측보다 측정이 이김)' — notion _RENDER_CSS_DIFF.md §1~9, 커밋 176a540~9f57677"
  - "ledger/2026-07.md 2026-07-17 measured-css-porting(강화) — '실측 근거 없는 px 금지 규율이 과보정 2회(컬럼폭 878 시도·title 패딩)를 즉시 롤백시킴. 추측 메모(TableView는 짧은 포맷) 실측 정정 사례 축적' — notion W-BY·W-CF 보고"
  - "status/notion.md 2026-07-17 새벽 'CSS 실측 포팅 완료'(W-BN, push 176a540) — '실물 computed 실측 결과 콜아웃 스타일 반전 발견·수정(실물=투명bg+테두리, 클론=회색채움), 폰트스택 정정, 구분선색 통일... 제목 잘림 = CSS 아닌 구조 갭(클론 input vs 실물 h1 contenteditable — input은 줄바꿈 불가) → T59 티켓' — 값 포팅과 구조 판별을 실측이 함께 갈라낸 사례"
  - "260615_canvas-clone 세션21 ①핸들·비디오플레이어 리트로핏(커밋 3ab442a, runs/2026-07-17-canvas-structfirst.md) — 실물 노드를 live CDP `getComputedStyle`+`outerHTML` verbatim 실측 후 클론에 그대로 이식(좌우 오프셋 10/28px→18px 통일, 세로간격 36→34px, 중앙Play 56→36px, 컨트롤바 인셋 0→8px 등) — 골격 단일화(2레이어→단일배지)와 동시 수행된 canvas측 실증"
  - "techniques/structure-first-cloning.md §순서 원칙 2 — '스타일: 골격이 같으면 computed 값·셀렉터 규칙을 거의 그대로 이식([[techniques.measured-css-porting]]) — 보정 불필요'"
updated: 2026-07-17
owner: 박춘순
---

# 실측 CSS 포팅 (골격 동치 후 computed 값 그대로 이식)

**한 줄**: [[techniques.structure-first-cloning]]의 ②스타일 단계. 골격(태그·role·부모-자식 그룹핑)이 실물과 이미 동치인 노드에 한해, [[techniques.dom-first-measurement]]로 실측한 computed 값·셀렉터 규칙을 **보정 스택 없이 그대로** 이식한다.

## 언제 쓰나
구조 게이트(①골격 단계)가 이미 통과한 노드에 한해. 골격이 안 맞은 채로 스타일 값부터 맞추면 이 기법이 아니라 [[techniques.structure-first-cloning]] §함정의 "보정 스택"이 된다 — 순서를 건너뛰지 않는다.

## 왜 (골격 동치 후에만 유효)
- 골격이 같으면 같은 셀렉터가 같은 요소에 걸리므로, computed 값을 즉시 이식해도 어긋날 이유가 구조적으로 없다 — "보정 없이" 맞는다는 게 이 기법의 핵심 전제다.
- 반대로 골격이 다른 채로 값만 맞추면, 요소 A의 오차를 요소 B의 마진으로 상쇄하는 보정 스택이 쌓인다. 특정 상태에선 픽셀이 맞아도 내용이 바뀌면 깨진다 — notion 캠페인이 이 대가를 실제로 치렀다(PLAYBOOK.md §2-①, [[techniques.structure-first-cloning]] §함정).
- notion 실증(2026-07-17): "실측 근거 없는 px 금지" 규율이 없었을 때 과보정 시도(컬럼폭 878px, title 패딩)가 나왔고, 규율 도입 후 즉시 롤백됐다 — "TableView는 짧은 포맷일 것"같은 서술적 추측도 실측이 매번 정정했다.

## 어떻게
1. 대상 노드의 골격이 구조 게이트를 통과했는지 먼저 확인한다([[techniques.structure-first-cloning]] exit gate).
2. [[techniques.dom-first-measurement]]로 실물 노드의 computed 값(색상·크기·여백·폰트·보더·radius 등)을 직접 덤프한다 — 추측 치수 0.
3. 같은 셀렉터/규칙을 클론 쪽 동일 골격 노드에 그대로 이식한다. 인접 요소 마진으로 상쇄하는 임의 보정값은 넣지 않는다.
4. attribute-diff 카운트가 수렴 방향으로 감소하는지 확인한다(PLAYBOOK.md §1.3 exit gate). 증가하거나 정체하면 "골격이 실은 안 맞았다"는 신호로 되짚는다.

notion 사례(`_RENDER_CSS_DIFF.md` §1~9, 커밋 176a540~9f57677)에서는 이 파이프라인 하나로 오너 육안지적 8건 + DB 3축 + 잔여갭 5건 + 풀블록 5건을 전부 해소했고, 부산물로 가설반증 3건(컬럼순서=가나다순, 아웃라인=고정비율, status칩=그룹 고정 3색)을 얻었다 — 문서·추측보다 측정이 이겼다.

## 함정
- **골격을 확인하지 않고 값부터 포팅하면 이 기법이 성립하지 않는다.** "computed 값이 일치"와 "보정 스택으로 우연히 픽셀이 맞음"은 겉보기에 구분되지 않으므로, 반드시 구조 게이트를 먼저 통과시킨 노드에만 이 기법을 적용한다 — 이게 [[techniques.structure-first-cloning]] §2-① 최대 실수의 재발방지 규칙 그 자체다.
- **CSS로 보여도 실은 구조 갭인 경우가 있다.** notion 사례: 제목이 잘려 보여 padding 등 CSS 값을 조정하려 했으나, 실측 결과 실물은 `<h1 contenteditable>`인데 클론은 `<input>`이라 애초에 줄바꿈이 불가능한 구조 문제였다(W-BN, push `176a540`). 값을 포팅하기 전에 "정말 스타일 문제인가, 태그/role 문제인가"부터 실측으로 갈라야 한다.
- 실측 없는 px 값(추측·"이 정도면 되겠지")은 금지 — 과보정 사례(컬럼폭 878px 시도, title 패딩)가 실제로 발생했고, 규율 도입 후에야 즉시 롤백되는 방식으로 잡혔다.

## 검증 (구조 게이트와 쌍으로)
이 기법 단독으로 "완료"를 선언하지 않는다. attribute-diff 수렴 + [[techniques.pixel-diff-baseline]](픽셀 배지) + 구조 게이트 3축이 함께 통과해야 한다([[techniques.structure-first-cloning]] §순서 원칙 3). 픽셀 배지만 오르는 건 이 기법이 아니라 §함정의 보정 스택일 수 있다.

## 관련
- [[techniques.dom-first-measurement]] — 이 기법이 쓰는 실측 수단(1차 오라클)
- [[techniques.structure-first-cloning]] — 이 기법이 속한 상위 순서 원칙(①골격→②스타일→③동작) 중 ②단계
- [[techniques.pixel-diff-baseline]] — 이 기법의 결과가 실제로 수렴했는지 확인하는 검증 축(구조 게이트와 쌍으로만)
