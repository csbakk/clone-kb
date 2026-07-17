---
id: techniques.total-fidelity-cloning
title: Total-Fidelity 클론 (전 서브시스템·전 층 계약 일치 — B 원칙)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.structure-first-cloning, techniques.measured-css-porting, techniques.dom-first-measurement]
evidence:
  - "오너 결정(2026-07-17): 클론 목표를 '화면만 같게'에서 '전부 같게'로 격상 — 체인 깊이·상태 메커니즘까지 실물과 완전 일치(B), 픽셀 등가 절충 안 함"
  - "260615_canvas-clone/ref/_SKELETON_CHAIN_MATRIX.md §2-2 — 프롬프트 입력 hover 전이: real=mount/unmount+reflow(리치에디터 인스턴스 교체) vs clone=상시마운트+opacity/pointerEvents 토글. 최종 픽셀은 등가로 수렴하나 메커니즘 자체는 다름 — 세션19는 이를 '무해 단순화'로 절충 판정했고, 이 카드는 그 절충을 B 미달 항목으로 재분류"
  - "260615_canvas-clone/ref/_SKELETON_CHAIN_MATRIX.md §2-1 — 체인 층수 real 13(+decorator 형제1) vs clone 10, Lexical류 decorator/스크롤 래퍼 미이식을 '무해'로 판정"
  - "260615_canvas-clone/ref/_STRUCTURE_FIRST_ROADMAP.md §4 — 핸들/엣지/툴바 골격 대조 커버리지 갭(RIP 델타 파일 없음, 프레임워크 표준사용 추정만 하고 실측 대조 없음) 명시적 기록"
  - "clone-kb/techniques/structure-first-cloning.md — 골격→스타일→동작 3단 원칙(오너 1순위 채택, 2026-07-17)의 확장. structure-first는 '가시·상호작용 층 99%'를 목표로 했고 잔여 1%를 '복사 불가능물'로 재구현 대상 처리했으나, B 원칙은 상태 메커니즘·API 계약처럼 '복사는 가능하나 지금까지 절충해온 층'까지 대상에 넣음"
updated: 2026-07-17
owner: 박춘순
---

# Total-Fidelity 클론 (B 원칙)

**한 줄**: 클론은 **화면만이 아니라 전 서브시스템을, 모든 층에서, 실물의 계약대로** 복제한다. 픽셀·기능이 등가로 수렴한다는 이유로 골격·상태 메커니즘·데이터 계약의 차이를 "무해 단순화"로 절충하지 않는다 — 프로들이 이유 있게 만든 층 구조를 그대로 따라가야, 실물이 기능을 추가할 때 클론이 따라간다.

## A vs B — 왜 절충을 그만두나

- **A(픽셀/기능 등가)**: 최종 렌더·동작 결과가 같으면 내부 구현 차이는 무해 판정. [[techniques.structure-first-cloning]]이 canvas retrofit에서 실제로 이 판정을 여러 번 내렸다 — 예: 프롬프트 입력 hover 전이가 real은 리치에디터 인스턴스를 mount/unmount하는데 clone은 상시-마운트+opacity 토글이지만, 최종 픽셀이 겹침 없이 같아서 "무해"로 종결(`_SKELETON_CHAIN_MATRIX.md` §2-2 판정 §9).
- **B(전층 일치)**: 오너가 2026-07-17 채택. 최종 결과가 같아도 **메커니즘 자체가 다르면 갭**이다. 이유: 실물이 나중에 그 상태 메커니즘에 새 기능을 얹으면(예: hover 시 리치에디터 인스턴스가 바뀌는 지점에 새 서브컴포넌트 추가), mount/unmount 아키텍처가 없는 클론은 그 확장을 못 따라간다 — 지금 등가인 결과값이 아니라 **미래 변경에 대한 구조적 추종 가능성**을 산다.
- **결론**: 이 카드 이후 "무해 단순화" 판정은 구조 갭 매트릭스에서 **B 재분류 대상**으로 다시 열린다. `structure-first-cloning`의 골격 원칙은 유지하되(①②③ 순서), 대상 범위를 §2 목록 11차원으로 확장한다.

## 11개 차원 (각각: 무엇을 뜨나 · 어떻게 측정 · 게이트 · canvas 현재상태)

범례: ○=계약 일치 확인·전용 게이트 존재 / △=부분 확인·전용 게이트 없음(부수 캡처만) / ✗=미측정·근거 없음

| # | 차원 | 무엇을 뜨나 | 어떻게 측정 | 게이트 | canvas 현재 |
|---|---|---|---|---|---|
| ① | 골격 | DOM 조상체인 — 층·태그·a11y role·"그 층의 담당"(border/배경/contenteditable 경계/overflow) | `harness/rip_chain.py`(잎→root 전 층 덤프) + [[techniques.dom-first-measurement]] | 구조 게이트: RIP 태그/role/그룹핑 자동 매칭 0 미스매치 | △ — top3 중 2건 해소(헤더span·라이트박스메타 존재), 프롬프트 골격은 리프 태그(`contentEditable role=textbox`)까지는 일치했으나 잔존 3~4층차·라이트박스 배치(aside vs foot)가 여전히 남음 → B 대상 |
| ② | 스타일(computed·상태별) | 상태별 `getComputedStyle` 전 속성 | RIP 레이어①(`rip_dump.py`) + [[techniques.measured-css-porting]](골격 일치 후 이식) | attribute-diff 카운트 수렴(현재 17,113, [[pipelines.99-percent]] 축) | ○ — 표준 기법으로 상시 가동, 세션마다 수렴 추적 중 |
| ③ | 동작/상태머신 | 이벤트→전이 경로, mount/unmount vs 스타일토글 분류, 단축키·드래그·undo·선택·포커스 | `harness/rip_state_diff.py`(경로 diff, 마운트/언마운트/스타일변경 3분류 — 세션19 신규) | 전이 **메커니즘 분류 일치**(mount/unmount+reflow인지 opacity토글인지까지 같아야 통과 — 결과값 동일은 불충분) | **✗ — B 미달 확정**. 프롬프트 hover(real=인스턴스 mount/unmount+reflow, clone=상시마운트+opacity/pointerEvents)가 대표 사례. 지금까지 "무해"로 절충됐던 바로 그 항목 |
| ④ | 데이터모델/직렬화 | 노드/doc JSON, 엣지, 클립보드 스키마 | [[techniques.canvas-clipboard-localstorage]], [[techniques.clipboard-source-of-truth]] | 왕복 diff 0([[techniques.cross-paste-parity]], verified) | ○ — 클립보드 계약은 이미 실측 확정·검증 완료 |
| ⑤ | 네트워크/API 계약 | 요청/응답 shape, 폴링 주기, auth 흐름 | 없음 — CDP Network 도메인 캡처 확장 필요(신규 도구) | 계약 스키마 diff 0(미구축) | **✗ — 전용 검증 전무**. GENERATE류는 MCP 경유라 클론 자체 프론트-백엔드 계약 대조가 시도된 적 없음 |
| ⑥ | 알고리즘(레이아웃/Tidy·엣지라우팅·줌수학·렌더티어) | 좌표 계산식, 엣지 path 생성 규칙, 줌-좌표 변환 | 좌표 재배치는 [[techniques.canvas-coord-inject-rearrange]](verified)로 일부 커버 | 좌표 재현 오차 임계치 | **✗ — 핸들/엣지/툴바 골격조차 미검증**(`_STRUCTURE_FIRST_ROADMAP.md` §4 커버리지 갭 명시. `rip_dump.py`가 className 미캡처라 `<Handle>` 특정 불가) |
| ⑦ | 타이밍/애니메이션 | 트랜지션 duration·이징·hover 스왑 타이밍 | [[techniques.animation-ripper]](experimental, 트랜지션 지문) | 이징/duration diff 임계치(미확정) | △ — 카드는 있으나 `proven_in: []`, canvas에 적용된 적 없음 |
| ⑧ | 렌더티어/성능 | zoom→render-mode 전이, 가상화/지연로딩 임계값 | 없음 | 미구축 | **✗ — 근거 없음** |
| ⑨ | 접근성(ARIA·포커스·키보드) | role/aria 속성, 포커스 트랩, 키보드 내비 | `rip_chain.py` 체인 덤프가 role을 부수적으로 캡처 중(전용 감사 아님) | role diff 0(골격 게이트에 종속, 전용 a11y 게이트 없음) | △ — role 일치는 골격 대조의 부산물로 상당수 확인됨(예: 라이트박스 `role=dialog`, 모델피커 `role=dialog` 일치), 포커스 트랩·키보드 내비는 미검증 |
| ⑩ | 에러/경계 | 입력 필터·검증 규칙·제한·재시도 정책 | 없음 | 미구축 | **✗ — 근거 없음** |
| ⑪ | 지속성/동기화 | autosave 주기, localStorage/서버 동기화 규칙 | [[techniques.atomic-localstorage-inject]](verified, notion), [[techniques.persist-migration-safety-net]](experimental, notion) | invariant 검증+백업 게이트 | △ — 두 기법 다 `proven_in: [notion]`뿐, canvas 미적용. localStorage 주입은 "테스트 하네스 주입" 목적이라 클론 자체의 autosave 계약 검증과는 결이 다름 |

## 크로스툴 재사용

- `rip_chain.py`/`rip_state_diff.py`(③·①의 측정 도구)는 canvas 세션19에서 신설됐지만 DOM 조상체인·상태 diff 추출이라는 방식 자체는 앱 종류에 무관 — notion·akiflow에도 그대로 이식 가능(react-flow 같은 특정 프레임워크 의존 없음).
- ⑤네트워크/API 계약·⑧렌더티어/⑩에러경계는 세 캠페인(canvas/notion/akiflow) 전부 미구축 — 어느 캠페인에서 먼저 시도하든 이 카드에 결과를 append하면 다른 캠페인이 그대로 재사용.
- ④데이터모델/⑪지속성 기법은 이미 notion(persist-migration-safety-net)·canvas(clipboard)로 반쪽씩 나뉘어 검증됨 — 서로의 검증을 교차 이식하면 양쪽 다 즉시 proven_in 확장 가능(신규 실측 불필요, 카드 통합만).

## 적용 시 원칙

1. **재센서스 아님**: 이미 골격 갭은 매트릭스(`_SKELETON_CHAIN_MATRIX.md`)와 `rip_chain.py` 산출물로 위치가 파악돼 있다. B 원칙은 "다시 찾으라"가 아니라 "이미 찾아놓고 절충했던 것을 닫으라"는 재분류 지시다.
2. **블록 단위 점진**: [[techniques.structure-first-cloning]] §함정의 경고("골격 리팩터는 렌더러 심장부") 그대로 승계 — 리스크 낮은 블록(신규 섹션 추가류)부터, 렌더러 심장부(상태 메커니즘 재작성)는 게이트망 선행 후 마지막.
3. **등가절충 금지의 실무적 의미**: "지금 결과가 같다"는 이유로 항목을 닫지 않는다. 닫으려면 ①~⑪ 표의 해당 행이 ○가 돼야 한다.
