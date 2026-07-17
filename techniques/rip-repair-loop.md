---
id: techniques.rip-repair-loop
title: RIP 레이어③ 자동 수복 루프
doctype: technique
status: verified
proven_in: [canvas, notion]
related: [techniques.rip-css-dump, techniques.rip-crawler, pipelines.rip-v1, techniques.structure-first-cloning]
evidence:
  - "260615_canvas-clone/ref/_RIP_MASTER_DELTA.md §4 — 티켓 그룹 4분류(판단필요/구현명확/시각확인필요/하네스자체버그), harness/rip_resweep_clone.py로 클론만 재덤프해 재검증"
  - "260615_canvas-clone/ref/_RIP_MASTER_DELTA.md §8 RIP-T-E — --radius-btn/--radius-pill 토큰 분리 사례 (1차 과잉교정 → 재측정 → 수정)"
  - "260622_notion-clone/RIP-PIPELINE.md — 델타 리포트가 티켓 배치로 이어짐, 재수렴 확인"
  - "260615_canvas-clone 세션17(2026-07-16) — 측정 전 window-size 정합 선행(→ [[techniques.dom-first-measurement]])이 22,626 중 −3,558을 하네스 노이즈로 분리, 남은 진짜갭 3건(줌바·Share·ref-add)만 수복해 17,490 확정. '노이즈 분리 후 수복'이 새 표준 절차로 굳어짐"
  - "260615_canvas-clone 세션19(2026-07-16) — 진짜갭 3건(folder-modal·assets-tab·topbar chevron) 17,490→17,425 역행0·0크레딧. ★`rip_delta_cluster` 확신 티켓 위양성률 高 재확인(~24건 조사 중 실제갭 소수) — 클러스터 순위 대신 상태별 delta.md 직접 훑기가 더 유효함을 Track C 트리아지가 실증"
  - "260615_canvas-clone 세션21(2026-07-17) — [[techniques.structure-first-cloning]] retrofit 선행 재덤프: 클론 5175 탭 4개 동시 상주로 url_substr 매칭 모호성 위험 상태였던 것을 state-spec 19개+resweep 하네스 2개를 canvas-id(3ad36980c5eb)로 영구 고정, 뷰포트 1556x895 정규화 후 재립. 17,425→17,113(-312, isolated 순수차분), 미니툴바 radius·out-of-view 토스트 유령 2건 종결. 이후 산출물탭 오염을 harness 레벨에서 원천차단"
updated: 2026-07-17
owner: 박춘순
---

# RIP 레이어③ 자동 수복 루프

**한 줄**: 레이어①/②가 낸 델타 리포트를 티켓 배치로 묶어 수정 → 클론만 재덤프해서 델타가 실제로 줄었는지 재검증 → 수렴할 때까지 반복.

## 어떻게
1. 델타 리포트를 4개 그룹으로 분류 (canvas `_RIP_MASTER_DELTA.md` §4 실제 분류 체계):
   - Group 1: 사람 판단 필요 (구현 전 확인)
   - Group 2: 구현 명확 (바로 수정)
   - Group 3: 시각 확인 필요
   - Group 4: 하네스/방법론 자체 버그 (제품 코드 문제 아님)
2. Group 2/3부터 수정 배치 실행.
3. `rip_resweep_clone.py`로 **클론만** 재덤프 (실물은 안 건드림 — 비파괴 원칙 유지, 재측정 비용도 절감).
4. 델타 재계산, 목표 수렴까지 반복.

## 실증 사례 — 과잉교정을 재측정이 잡은 케이스
canvas RIP-T-E: 델타 리포트가 "border-radius 999px가 여러 곳에서 어긋난다"고 지적 → 1차 수정에서 `999px→99px` 일괄 치환 → 재덤프하니 `.hf-toolbar`(실제로 999px이 맞는 컴포넌트)가 깨짐 → 원본 JSON 재측정으로 확인 후 `--radius-btn`(99px)과 `--radius-pill`(999px) 토큰을 분리하는 걸로 최종 수정. **이 루프가 없었다면 "고쳤다고 착각한 채 다른 걸 깨뜨린" 상태로 넘어갔을 것.**

## 결과
- canvas: attribute-diff 38,476 → 30,580 (-20.5%), 남은 델타는 커서 불일치(740), fontWeight(620), 색상 근사(#fff↔#f7f7f8, ~3,400), display/position(~1,600) 등으로 카테고리화 — "시스템 토큰으로 못 잡는 컴포넌트별 케이스워크" 영역으로 남김.
- notion: 캘린더 뷰 157→18(-88.5%), title_hover 29→0(완전 수렴), date popup 152→27(-82.2%).

## 함정
- 전역 치환(global find-replace) 방식의 수복은 항상 다른 곳을 깨뜨릴 위험을 동반 — 반드시 재덤프 재검증 없이는 "완료" 선언 금지.
- Group 1(판단 필요)을 건너뛰고 바로 구현하면 위와 같은 과잉교정 재발 가능성 높음.
- ★**클러스터 기반 "확신 티켓" 우선순위의 위양성률이 높다** (canvas 세션19, 2026-07-16). `rip_delta_cluster`가 상위로 승격시킨 확신 클러스터를 조사해보면(~24건 표본) 실제 진짜갭인 것은 소수이고, 나머지는 하네스 노이즈·캡처 아티팩트·오매칭 클러스터인 경우가 많다 — 클러스터 크기(diff 건수)가 커 보인다고 "확신도"가 높은 게 아니라 오히려 반복되는 노이즈일수록 큰 클러스터로 뭉쳐 순위 상단을 차지하는 경향이 있음. **대응**: 클러스터 순위를 1차 필터로 신뢰하지 말고, ①상태별 delta.md를 처음부터 직접 훑기 ②발견 항목을 product(진짜 코드갭)/harness(측정도구 문제)/캡처노이즈(창크기·타이밍 등) 3분류 게이트에 통과시킨 것만 티켓화. 클러스터는 "탐색 보조"로만 쓰고 "확신"의 근거로 쓰지 않는다.

## 관련
- [[techniques.rip-crawler]] — 이 루프가 다루는 델타의 또 다른 원천 (인터랙션 오분류)
- [[techniques.visual-triage-sheet]] — 클러스터/모호 티켓을 사람이 판단 가능한 형식으로 바꾸는 후속 단계(이 카드의 위양성 문제를 시각 증거로 보완)
