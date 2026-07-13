---
name: clone-verify
description: 클론 작업을 "완료"로 표시하기 전 적대적으로(빌더≠검증자) 재검증한다. "이거 진짜 끝났는지 검증해줘", "적대적으로 재검증해줘", "verify-first로 확인해줘" 같은 요청, 또는 게이트/티켓을 닫기 직전에 사용.
status: draft (레포 동봉, 설치는 미실행 — 검토 후 다음 단계에서 설치)
based_on: techniques.adversarial-verification, techniques.orchestrator-model-routing, techniques.regression-harness-suite, pipelines.verify-first-loop
---

# clone-verify

## 트리거
- "이 티켓/게이트 닫아도 되는지 검증해줘"
- 빌더 서브에이전트가 "완료했다"고 보고한 직후 (자동으로 이 스킬을 걸어야 함 — 자가선언을 그대로 신뢰하지 않는다)

## 핵심 원칙
**빌더의 "완료" 자가선언을 신뢰하지 않는다. 처음부터 다시 측정한다.** ([[techniques.adversarial-verification]])

## 절차

### 1. 검증자 컨텍스트 분리
가능하면 빌더와 다른 모델/다른 세션으로 검증한다. 최소한 검증자 모델 티어는 빌더 이상이어야 한다([[techniques.orchestrator-model-routing]] — 이 규칙은 canvas 캠페인에서 명문화됨, 다른 캠페인은 "역할 분리"까지만 확인됨을 참고).

### 2. 재측정 (빌더 코드/로그를 읽지 말고 직접 실행)
- 기존 회귀 스위트 재실행: `python harness/_b*_verify.py` 또는 `*_gate.py` 전체([[techniques.regression-harness-suite]]).
- 이 티켓이 새로 추가한 기능이면, 그 기능 전용 검증 스크립트가 없는 경우 이번에 하나 만들어 스위트에 편입.
- 실물과의 대조가 필요하면 [[techniques.adversarial-verification]]의 동일-오라클-이중실행 패턴(같은 제스처를 실물·클론 두 세션에 동시 실행 후 diff) 사용.

### 3. 수치로 판정, 감(感) 금지
- "대충 맞는 것 같다"는 통과 사유가 될 수 없다. 스크립트 출력(PASS/FAIL, diff 개수, %)만 근거로 삼는다.
- 결정적 계산(수치 diff)은 스크립트로, 판단이 필요한 부분(디자인 의도 일치 여부 등)만 에이전트 판단([[techniques.subagent-fanout-rules]] 규칙3/4).

### 4. 반려 시
반려 사유를 구체적으로(어느 파일, 어느 속성, 기대값 vs 실제값) 남기고 빌더에게 돌려보낸다. 통과할 때까지 이 스킬을 다시 건다.

### 5. 통과 시
- append-only 로그에 "검증됨" 기록 (누가/언제/무슨 스크립트로).
- 무인 야간 런 중이면 이 결과가 곧 "디스크 산출물"이 되어 다음 사이클의 완료판단 근거가 됨([[techniques.night-run-sop]]).

## 종료 조건
독립 재측정 스크립트가 PASS를 리포트하고, 그 결과가 append-only 로그에 남았을 때만 "완료"로 표시.

## 근거 카드
[[techniques.adversarial-verification]] · [[techniques.orchestrator-model-routing]] · [[techniques.regression-harness-suite]] · [[techniques.append-only-logging]] · [[pipelines.verify-first-loop]]
