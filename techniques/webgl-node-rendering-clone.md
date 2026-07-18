---
id: techniques.webgl-node-rendering-clone
title: WebGL 노드 렌더 대응 (DOM 골격 없는 캔버스 노드 클론)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.structure-first-cloning, techniques.coordinate-click-capture, techniques.canvas-clipboard-localstorage, techniques.version-archive-3layer, techniques.total-fidelity-cloning]
evidence:
  - "260615_canvas-clone ref/real-recapture-2026-07-18/_FINDING-webgl-migration.md (2026-07-18) — 실물 Higgsfield Canvas가 노드를 DOM이 아니라 WebGL `<canvas>`에 픽셀로 렌더하도록 업그레이드된 것을 확정. 증거: 뷰포트 전체 WebGL `<canvas>`(`getContext('webgl')` 성공) 존재, `.react-flow__nodes`/`.react-flow__edges` 컨테이너 children 0, `.react-flow__node` 셀렉터 매치 0, 노드 텍스트(프롬프트 'warm morning coffee')가 `document.body.innerText`에 부재 — 화면엔 보이지만 DOM엔 없음"
  - "260615_canvas-clone ref/real-recapture-2026-07-18/_DECISION-dom-vs-webgl.md (2026-07-18) — 오너 결정: 클론은 DOM/@xyflow 유지(A안). 근거: WebGL의 유일한 실질 이득=대규모(수백 노드) 성능인데 클론은 그 제약이 없고, 대가(검사·측정·CSS포팅·자동화 불가, 접근성 상실, 그래픽스 전문성 필요)가 방법론 핵심(DOM 판독 기반 구조-우선 클론)을 정통으로 침. 재고 조건: '영화·드라마 제작에서 한 캔버스에 수백 장면 노드'를 실제로 놓아야 할 때만 노드 렌더 레이어만 스왑(데이터모델·상태·인스펙터·셸·동작 스펙은 재활용)"
  - "260615_canvas-clone ref/real-recapture-2026-07-18/menus/_NODE-INVENTORY.md (2026-07-18) — Add-node 메뉴의 노드 타입 9~11종이 구버전 번들(2026-06-09)과 동일함을 확인: 타입/데이터모델은 WebGL 이관에도 안 바뀌고 **렌더 방식만** DOM→WebGL로 바뀜"
updated: 2026-07-18
owner: 박춘순
---

# WebGL 노드 렌더 대응 (DOM 골격 없는 캔버스 노드 클론)

**한 줄**: 클론 대상이 캔버스/노드 UI를 **WebGL로 렌더**(Figma·Miro류 하이브리드 = React DOM 셸 + WebGL 노드 레이어)하면 노드에는 **애초에 DOM 골격이 존재하지 않는다** — [[techniques.structure-first-cloning]](골격→스타일→동작)이 노드 층엔 적용 불가. 셸/툴바/인스펙터/메뉴는 여전히 DOM이라 그대로 캡처 가능.

## 감지 (3-신호, 전부 만족해야 확정)
1. 노드가 그려지는 영역에 **뷰포트 전체 크기 `<canvas>`**가 있고 `getContext('webgl')`(또는 `webgl2`)이 성공한다.
2. 노드 컨테이너(예: `.react-flow__nodes`)의 **children이 0**이다 — 프레임워크 스캐폴드는 남아있지만 노드 엘리먼트가 없음.
3. 노드 텍스트(프롬프트 내용 등)가 `document.body.innerText`/DOM 어디에도 **없다** — 화면엔 보이는데 텍스트 검색 0건.

3개 다 참이면 "노드는 WebGL 픽셀"로 확정. 하나라도 어긋나면(예: children>0인데 스타일만 다름) 이건 그냥 스타일 갭이지 렌더 아키텍처 갈림이 아니다 — [[techniques.structure-first-cloning]] 표준 경로로 처리.

## 함의
- **노드 DOM 골격/조상체인/CSS 복사가 원천적으로 불가능** — 복사 대상 DOM 자체가 없다(WebGL 픽셀이라 서버가 아니라 GPU가 그린다). 기존에 실물 DOM을 실측해 클론 CSS로 이식하던 파이프라인(RIP 등)은 노드 층에서 재적용 불가 — 그 결과물은 "구버전(DOM 노드) 기준"으로 태깅해 보존만 한다.
- **셸/툴바/인스펙터/메뉴는 여전히 DOM** — 노드 렌더 아키텍처 변경이 앱 전체에 전파되지 않는다. 이 부분은 기존 구조-우선 방법론이 그대로 적용됨.
- 노드 **타입/데이터모델은 렌더 방식과 독립** — WebGL 이관 전후로 Add-node 메뉴의 노드 타입 목록이 그대로였다(§evidence). 렌더가 바뀌어도 데이터 계약은 안 바뀔 수 있다는 뜻이므로, 데이터모델 캡처는 렌더 판별과 무관하게 항상 유효.

## 캡처 전략 (노드 = WebGL일 때)
DOM이 없으니 3갈래로 나눠 대체한다:
- **데이터모델**: 클립보드/localStorage(Select-All+Copy → `{nodes,edges,results}` JSON) — [[techniques.canvas-clipboard-localstorage]]. 노드 구조·파라미터·결과를 authoritative하게 담는다.
- **시각(픽셀)**: 스크린샷(컴포지터 레벨). `canvas.toDataURL()`은 `preserveDrawingBuffer` 없이는 빈 이미지라 못 쓴다 — 반드시 화면 캡처로.
- **인터랙션**: 노드에 DOM 타겟이 없으므로 화면 좌표 기반 클릭으로 대체 — [[techniques.coordinate-click-capture]]. 노드 클릭 → 우측 인스펙터 패널이 열리면 그 패널은 다시 DOM(`.canvas-node-state-form`류)이라 통상 방법으로 캡처 가능.

3층을 겹쳐 쓰는 아카이브 절차는 [[techniques.version-archive-3layer]] 참고.

## 클론 전략 — DOM 유지, WebGL 안 쫓음 (오너 채택 A안, 2026-07-18)
- 클론은 **DOM/@xyflow(react-flow) 유지**. WebGL 전환(전 노드 렌더 재작성)은 대규모 재작업 대비 이득이 지금 규모(수십 노드)에선 없다 — WebGL의 유일한 실질 이득은 대규모(수백 노드) 성능인데, 그 이득의 대가(검사·측정·CSS 포팅·자동화 불가, 접근성 상실, 셰이더/씬그래프 전문성 필요)가 정확히 이 KB의 클론 방법론이 의존하는 것들을 친다.
- **재고 조건(오너 통찰)**: "안 함"이 아니라 "때가 되면" — 우리 스스로 DOM의 대규모 성능 한계에 부딪히는 지점(예: 영화·드라마 제작에서 한 캔버스에 수백 장면 노드)에 도달하면, 그때 **노드 렌더 레이어만** WebGL로 스왑한다. 데이터모델·상태·인스펙터·셸·동작 스펙은 재활용되므로 "전부 다시"가 아니라 좁은 범위 전환.
- 미리 최적화하지 않는다 — 병목이 실제로 나면 그때.

## 함정
- **"DOM 개발 후 컨버팅"은 대체로 신화**: 임의 CSS/DOM → WebGL 자동 변환은 없다. `<div>` flexbox가 저절로 GL로 안 간다. 진짜 있는 것은 React 선언형으로 WebGL 렌더러 라이브러리(`react-konva`·`react-three-fiber` 등)에 노드 컴포넌트를 **재작성**하는 것 — HTML/CSS 공짜 변환이 아니다. 나중에 WebGL로 갈 계획이라면 지금부터 노드 데이터/상태/동작 ↔ 렌더 표현을 분리해두면(react-flow가 원래 그런 구조) 전환 범위가 좁아진다.
- WebGL 노드의 **순수 시각 리스타일**(픽셀 룩 변화)은 쫓지 않는다 — 러닝머신 방지, [[techniques.baseline-then-diff]]의 "스냅샷은 아카이브만" 규율 적용.
- 3-신호 감지 없이 "노드가 좀 다르게 보인다"만으로 WebGL 이관을 단정하지 말 것 — 스타일 갭과 렌더 아키텍처 갈림은 대응 전략이 완전히 다르다.

## 관련
- [[techniques.structure-first-cloning]] — 이 카드의 발견이 그 원칙에 적용 범위 caveat를 추가하는 계기가 됨
- [[techniques.coordinate-click-capture]] — DOM 타겟 없는 노드를 좌표로 조작하는 대체 수단
- [[techniques.canvas-clipboard-localstorage]] — 데이터모델 캡처 메커니즘
- [[techniques.version-archive-3layer]] — 이 렌더 이원성(DOM 셸 + WebGL 노드)을 겹쳐서 박제하는 절차
- [[techniques.total-fidelity-cloning]] — "골격까지 실물과 동치화" B원칙과의 긴장(이 카드는 노드 렌더에 한해 예외를 둔 사례)
