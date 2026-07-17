---
id: techniques.clone-documentation-formats
title: 클론 문서화·시각화 포맷 가이드 (언제 무엇을 쓰나)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.interaction-state-map, techniques.structure-first-cloning, techniques.dom-first-measurement, techniques.state-spec-json, techniques.rip-crawler, techniques.visual-triage-sheet, techniques.regression-harness-suite]
evidence:
  - "260615_canvas-clone/reports/doc-formats-catalog.html + gen_doc_formats_catalog.py (private repo, 로컬뷰) — 16개 포맷을 canvas 이미지 Generate 노드 실측(mermaid stateDiagram/flowchart/sequenceDiagram/erDiagram/journey 5종 실렌더 + 표 6종)으로 예시화. 이 카드(PUBLIC)는 스샷·토큰 없이 방법론만, 예시는 그쪽 파일 참조"
  - "오너 실증 2026-07-17: '텍스트만이면 안 와닿는다 — 각 포맷을 실제 예시로 보여줘' 지시로 doc-formats-catalog.html 신설. 스샷+구조화표+mermaid 조합이 AI/사람 공통 판독에 가장 좋다는 판단 원문"
  - "260615_canvas-clone reports/gap-tests/gen_gallery.py, narrative-parity/gen_compare.py — 이 캠페인이 이미 실전에서 써온 '스샷+표+대조갤러리' 패턴이 이 카드가 명문화하는 규율의 선행 사례"
updated: 2026-07-17
owner: 박춘순
---

# 클론 문서화·시각화 포맷 가이드 (언제 무엇을 쓰나)

**한 줄**: 클론 정찰·검증·인수인계마다 "이번엔 뭘로 문서화하지"를 매번 새로 고민하지 않도록, 업계 표준 문서화/시각화 포맷을 **용도별로 분류**하고 **어느 파이프라인 단계에 맞는지**를 명문화한다. 실제 렌더 예시(mermaid·표·스샷 갤러리)는 이 리포가 PUBLIC이라 담지 않음 — `260615_canvas-clone/reports/doc-formats-catalog.html`(private repo, 로컬뷰) 참조.

## 왜 필요한가

클론 캠페인이 길어질수록(canvas는 세션 22+) 정찰 산출물의 형태가 세션마다 제각각이 된다 — 어떤 세션은 markdown 서술만, 어떤 세션은 표만, 어떤 세션은 스샷만. 오너가 "텍스트만이면 안 와닿는다"고 지적한 지점이 정확히 이것 — **포맷 선택 자체가 정찰 품질에 영향**을 준다. 이 카드는 "어떤 상황에 어떤 포맷"을 규율화해 매 세션 처음부터 고민하지 않게 한다.

## 업계 포맷 목록 — 무엇·언제

| 포맷 | 핵심 | 강점 |
|---|---|---|
| 상태 전이 다이어그램(state transition diagram) | 상태+전이조건 그래프 | "이 버튼 누르면 어디로" 한눈에 |
| 와이어플로우(wireflow) | 실제 화면(스샷) 박스를 흐름 순서로 배치+화살표 | 추상 다이어그램보다 화면이 먼저 와닿음(인수인계 강함) |
| 컴포넌트 상태 매트릭스(component state matrix) | 상태×트리거×DOM변화×스샷 표 | 상태 다이어그램의 각 노드를 행으로 펼침 — 구현 체크리스트로 그대로 사용 가능 |
| 인터랙션 인벤토리(interaction inventory) / UI 상태맵 | 클릭 가능한 것 전부의 평평한 목록 | 상태 그래프를 그리기 전 원자재, 정찰 1단계 |
| 유저/스크린 플로우(user/screen flow) | 사용자 목표 관점 화면 이동 상위 흐름도 | 컴포넌트 내부가 아니라 "어디서 어디로" 스코프 |
| 시퀀스 다이어그램(sequence diagram) | 시간순 액터간 이벤트/요청 | 타이밍이 중요한 생성/폴링 로직에 적합 |
| 데이터모델/ERD | 엔티티 관계 스키마 | 구조 정찰 — "무엇이 무엇을 참조하나"가 핵심인 도구 |
| API 계약 표 | 엔드포인트·요청/응답 shape | 프론트-백 경계가 있는 클론(백엔드도 직접 구현할 때) |
| 결정 표(decision table) | 입력조건 조합 → 결과 | progressive disclosure·비용 로직처럼 조건분기 정찰에 상태그래프보다 간결 |
| 어노테이티드 스샷/레드라인 | 스샷 위 번호 콜아웃+범례 | 디자이너-개발자 핸드오프 표준(Zeplin/Figma Inspect류) |
| Storybook류(컴포넌트 격리 카탈로그) | 컴포넌트를 상태별 개별 스토리로 | 회귀 스냅샷 자동화 후보 — 정적 스샷 갤러리로 동등 효과 대체 가능 |
| 저니맵(journey map) | 단계별 만족도/마찰 점수 | 제품 기획·오너 브리핑용(클론 정찰 파이프라인 자체엔 낮은 우선순위) |
| BPMN | 스윔레인+게이트웨이 승인 프로세스 | 멀티팀 승인 흐름이 있을 때만 — 1인 AI 주도 정찰엔 대개 과잉 스펙 |
| **스켈레톤 체인 매트릭스**(우리 자산) | 리프→root 조상 체인 층별 기록(태그·role·"이 층의 담당") | structure-first-cloning ①골격 단계 전용, real/clone 나란히 대조 |
| **RIP delta**(우리 자산, 기계용) | DOM 전수 덤프의 경로+bbox 자동 diff | 사람이 아니라 AI가 순회 판정하는 검증 게이트 원자재 |
| **인터랙션 상태지도**(이 캠페인 신설) | ①+②+③(상태전이+매트릭스+갤러리) 복합 | [[techniques.interaction-state-map]] 참조 |

## 용도별 선택 — 정찰 / 검증 / 인수인계 / AI 소비용

- **정찰(recon)**: 인터랙션 인벤토리 → 유저/스크린 플로우 → 결정 표 순으로 원자재부터 빠르게 확보.
- **구조(structure)**: 스켈레톤 체인 매트릭스 → ERD(단순화) — [[techniques.structure-first-cloning]]의 ①골격 단계.
- **상태(state)**: 상태 전이 다이어그램 → 컴포넌트 상태 매트릭스 → 시퀀스 다이어그램 — 동작 레벨, 타이밍까지.
- **검증(gate)**: RIP delta(기계용) → 컴포넌트 상태 매트릭스를 회귀 체크리스트로 재사용 — [[techniques.regression-harness-suite]]와 1:1.
- **인수인계(handoff)**: 인터랙션 상태지도(복합) → 와이어플로우 → 저니맵 — 화면이 먼저 보여야 새 합류자가 빠르다.

## ★AI(오케·빌더)가 잘 정리·이해하는 포맷 — 규율

오너 실증(2026-07-17): **스샷+표 조합이 AI 판독에 가장 좋았다** — "텍스트만이면 안 와닿는다"는 피드백이 이 카드와 `doc-formats-catalog.html`을 낳았다. 명문화된 규율:

1. **AI가 만들 때(사람도 같이 읽는 산출물)**: 정찰 보고서·인수인계 문서는 반드시 **스샷 임베드 + 구조화 표 + mermaid 다이어그램 조합**으로 — 텍스트 단독 서술 금지. 대조갤러리 톤(카드+썸네일+확대)이 이미 이 캠페인의 `gen_gallery.py`/`gen_compare.py`에서 검증된 패턴.
2. **AI가 소비할 때(게이트, 기계가 판정만 하면 되는 곳)**: 표보다 RIP delta류 **JSON/path-diff 구조화 데이터**가 낫다 — 표는 사람이 읽는 오버헤드, 기계는 구조 데이터를 직접 순회하는 게 더 빠르고 정확하다.
3. **같은 정보를 두 번 만들지 않는다**: 상태 매트릭스 한 벌(데이터 리스트)을 만들면 mermaid 다이어그램은 그 리스트의 parent/trigger 관계를 코드로 순회해 **자동 생성** — 손으로 다이어그램과 표를 각각 다시 그리지 않는다([[techniques.interaction-state-map]]의 `gen_map.py` STATES 패턴이 이 규율의 구현체).
4. **포맷과 진실성을 분리**: 실측 데이터가 없는 포맷(ERD·API 계약표·저니맵·레드라인 좌표 등)을 예시로 보여줄 땐 반드시 "예시(포맷 시연용, 실측 아님)"으로 라벨링 — 포맷 시연과 실측 근거를 섞어서 실측인 것처럼 보이게 하지 않는다.

## 우리 클론 파이프라인 매핑

```
정찰(recon) → 구조(structure) → 상태(state) → 검증(gate) → 인수인계(handoff)
   │              │                │              │               │
인벤토리       스켈레톤체인       상태전이        RIP delta      인터랙션 상태지도
유저플로우     ERD(단순화)       상태매트릭스     회귀체크리스트   와이어플로우
결정표                          시퀀스다이어그램                  저니맵(선택)
```

## 함정

- 포맷을 고르는 데 시간을 너무 쓰면 본말전도 — 위 매핑 표를 "질문"이 아니라 "기본값"으로 쓴다. 애매하면 정찰=인벤토리, 인수인계=인터랙션 상태지도로 시작해도 충분하다.
- PUBLIC 리포(이 KB) 규칙상 스샷·토큰은 절대 못 담는다 — 예시가 필요하면 항상 각 프로젝트 private repo에 `doc-formats-catalog.html`류 파일을 만들고 이 카드에선 경로 포인터만.

## 관련
- [[techniques.interaction-state-map]] — 이 카탈로그의 항목 중 하나(★이 캠페인 신설), 실제 파일럿 산출물
- [[techniques.structure-first-cloning]] — "구조" 단계 포맷(스켈레톤 체인 매트릭스)의 방법론적 배경
- [[techniques.dom-first-measurement]] — "픽셀 스샷 단독"이 아니라 "DOM/표 기반"이 더 신뢰도 높다는 선행 원칙, 이 카드의 §AI 소비용 규율과 같은 방향
- [[techniques.regression-harness-suite]] — 컴포넌트 상태 매트릭스가 회귀 체크리스트로 이어지는 실제 소비처
- [[techniques.visual-triage-sheet]] — 스샷+bbox 오버레이 조합이 사람 판독에 강하다는 선행 근거
