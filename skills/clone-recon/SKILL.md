---
name: clone-recon
description: 실물 웹앱을 비파괴로(리로드 없이) 정찰해 DOM/스타일/토큰/컨트롤 인벤토리를 뽑는다. "실물 정찰해줘", "이 화면 컴포넌트 스타일 뽑아줘", "peek 돌려줘" 같은 요청에 사용. 새 클론 캠페인을 시작할 때 첫 단계.
status: draft (레포 동봉, 설치는 미실행 — 검토 후 다음 단계에서 설치)
based_on: techniques.cdp-nondestructive-recon, techniques.dom-first-measurement, techniques.cdp-raw-driver, techniques.record-during-hover
---

# clone-recon

## 트리거
- "실물 앱 정찰해줘" / "이 화면 스타일/구조 뽑아줘" / "새 클론 캠페인 시작, 먼저 실물부터 봐줘"

## 안전경계 (최우선 — 절대 원칙)
1. **실물 세션은 리로드 금지.** attach만 한다([[techniques.cdp-nondestructive-recon]]).
2. **GENERATE/Delete/Share/Invite 등 과금·파괴적 액션은 절대 트리거하지 않는다.**
3. 상태를 바꾸는 클릭(열기 등)을 했으면 **반드시 원상복구**까지 하고 끝낸다.
4. 이 프로젝트 전용 CDP 포트/프로필([[techniques.port-profile-isolation]])로만 attach — 다른 프로젝트 세션과 섞이지 않게.

## 절차

### 1. attach
```
python3 harness/peek.py shot <label>       # 스크린샷 (육안 보조용)
python3 harness/peek.py dom <label>        # DOM 인벤토리 + computedStyle
python3 harness/peek.py tokens             # 디자인 토큰 (색상/폰트/spacing)
python3 harness/peek.py probe              # 컨트롤 인벤토리
```
attach가 180초 넘게 걸리면 좀비 탭 문제 — `cdp_raw.py` 기반 raw 드라이버로 전환([[techniques.cdp-raw-driver]]).

### 2. 정적 구조 측정 (DOM 우선, 픽셀은 보조)
`dom_snap.py` 류로 대상 subtree의 box+computedStyle을 덤프. 스크린샷은 육안 보조로만 남긴다([[techniques.dom-first-measurement]]) — 1차 오라클로 쓰지 않는다.

### 3. 동적 상태 측정 (hover/drag 등)
레코딩 시작 → 동작 수행 → 정지 → 변이 로그 읽기 (Clone Inspector `ci_agent.py` 또는 `dom_recorder.py`, [[techniques.record-during-hover]]). 위치 스캔(elementsFromPoint)은 보조로만.

### 4. 클릭 후 캡처 (비파괴 유지)
```
python3 harness/peek.py click "<selector>" <label>
```
클릭 → 캡처 → 반드시 닫기/취소로 원상복구.

### 5. 결과 정리
정찰 산출물(JSON/스크린샷)을 회차별 파일로 저장. 다음 단계(클론 구현 또는 [[techniques.rip-css-dump]] 전수 비교)의 입력이 됨.

## 종료 조건
정찰 목표 화면/상태의 스타일·구조·컨트롤 인벤토리가 확보되고, 실물 세션이 정찰 시작 전과 동일한 상태로 복원됨.

## 근거 카드
[[techniques.cdp-nondestructive-recon]] · [[techniques.dom-first-measurement]] · [[techniques.cdp-raw-driver]] · [[techniques.record-during-hover]] · [[techniques.port-profile-isolation]]
