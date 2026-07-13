---
name: clone-rip
description: 웹앱 클론 캠페인에서 실물 vs 클론의 구조적 델타를 전수(全數) DOM/CSS 덤프로 찾아내는 RIP 파이프라인을 구동한다. "이 클론이 실물이랑 얼마나 다른지 전체적으로 훑어줘", "RIP 돌려줘", "구조 델타 뽑아줘" 같은 요청에 사용.
status: draft (레포 동봉, 설치는 미실행 — 검토 후 다음 단계에서 설치)
based_on: techniques.rip-css-dump, techniques.rip-crawler, techniques.rip-repair-loop, pipelines.rip-v1
---

# clone-rip

## 트리거
- "RIP 파이프라인 돌려줘" / "구조 델타 얼마나 남았는지 봐줘" / "이 상태 전수 비교해줘"
- 새 클론 캠페인에서 체크리스트 실측을 벗어나 기계 전수 비교로 전환하고 싶을 때

## 절차

### 0. 사전 조건
- [[techniques.port-profile-isolation]] 준수: 이 프로젝트 전용 CDP 포트 + Chrome 프로필이 이미 떠 있어야 함.
- 실물 세션은 로그인된 상태로 attach만 할 것 — 리로드 금지([[techniques.cdp-nondestructive-recon]]).

### 1. 상태 명세 (없으면 먼저 작성)
`ref/rip/states/<state>.json`에 `real{}`/`clone{}` 병렬 블록 작성:
- `cdp`, `url`, `root_selector`, `actions[]`(도달 클릭시퀀스), `cleanup[]`(원상복구)
→ [[techniques.state-spec-json]] 카드의 템플릿 참고.

### 2. 레이어① 덤프
```
python3 harness/rip_dump.py <state.json 경로>
python3 harness/rip_align.py <real_dump> <clone_dump>
```
- 좀비 탭으로 attach가 180초 이상 걸리면 `cdp_raw.py` 기반 드라이버로 전환([[techniques.cdp-raw-driver]]).
- 출력: attribute-diff 목록 (구조 매칭 안 된 엘리먼트는 별도 집계).

### 3. 레이어② 크롤러 (선택 — 인터랙션까지 볼 때)
```
python3 harness/rip_crawl.py <state.json 경로>
python3 harness/rip_crawl_diff.py <real_graph> <clone_graph>
```
- `BLOCK_TEXT_SUBSTRINGS`(GENERATE/Delete/Share 등)와 `PROTECTED_NODE_SELECTORS`가 설정돼 있는지 반드시 확인 — 없으면 실물에 위험 액션이 실행될 수 있음.
- URL이 예상 범위를 벗어나면 즉시 중단·복구([[techniques.url-escape-guard]]).

### 4. 델타 리포트 → 티켓 배치
결과를 4개 그룹으로 분류: ①판단필요 ②구현명확 ③시각확인필요 ④하네스자체버그. ②③부터 수정.

### 5. 재검증 (레이어③)
```
python3 harness/rip_resweep_clone.py <state.json 경로>   # 클론만 재덤프, 실물은 안 건드림
```
델타가 실제로 줄었는지 확인 후에만 "완료" 표시. 전역 치환(find-replace)식 수정은 반드시 재덤프로 부작용(과잉교정) 확인.

### 6. 로그
결과를 append-only 워크로그에 기록([[techniques.append-only-logging]]) — 회차 번호, 델타 수치, 남은 카테고리.

## 종료 조건
델타가 목표 임계값 이하로 수렴하거나, 남은 델타가 전부 "시스템 토큰으로 안 잡히는 컴포넌트별 케이스워크"로 분류되어 개별 티켓화됨.

## 근거 카드
[[techniques.rip-css-dump]] · [[techniques.rip-crawler]] · [[techniques.rip-repair-loop]] · [[techniques.state-spec-json]] · [[techniques.cdp-raw-driver]] · [[techniques.url-escape-guard]] · [[pipelines.rip-v1]]
