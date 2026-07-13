---
id: pipelines.verify-first-loop
title: Verify-First 루프 (측정→대조→티켓→구현→검증→커밋)
doctype: pipeline
status: standard
proven_in: [canvas, notion, akiflow]
related: [techniques.adversarial-verification, techniques.orchestrator-model-routing, techniques.regression-harness-suite, techniques.append-only-logging, techniques.subagent-fanout-rules]
evidence:
  - "260615_canvas-clone/docs/2026-07-11-parity-rep-method.md §3 — ①측정→②대조(갭매트릭스)→③티켓→④구현→⑤검증→⑥커밋→①"
  - "260622_notion-clone/harness/ci_agent.py + ci_compare.py — 실물·클론 동시 측정 대조"
  - "260622_akiflow-clone/harness/gate.py — GATE PASS 3/3 최종 검증 게이트"
updated: 2026-07-13
owner: 박춘순
---

# Verify-First 루프 (측정→대조→티켓→구현→검증→커밋)

**한 줄**: 클론 캠페인의 범용 작업 단위 루프. "구현했다"가 아니라 "독립적으로 재측정해서 통과했다"를 완료 기준으로 삼는다. 3캠페인 전부에서 각자 다른 도구로 실증.

## 루프 조립도

```mermaid
flowchart LR
    M["① 측정<br/>실물 vs 클론<br/>DOM/computedStyle"] --> C["② 대조<br/>갭 매트릭스 = 작업 큐"]
    C --> T["③ 티켓화"]
    T --> I["④ 구현"]
    I --> V["⑤ 검증<br/>verify-first 서브에이전트<br/>빌더 ≠ 검증자"]
    V -->|통과| K["⑥ 커밋"]
    V -->|반려| I
    K --> M

    classDef step fill:#d1e7ff,stroke:#1c64c2,stroke-width:2px;
    classDef gate fill:#fff3cd,stroke:#b8860b,stroke-width:2px;
    class M,C,T,I,K step;
    class V gate;
```

## 검증 주체 확장 규칙
초기 렙(rep)은 메인 세션이 직접(수치+육안) 검증한다. 갭이 티켓 단위로 쪼개져 병렬 여지가 생기면 그때부터 [[techniques.adversarial-verification]] 서브에이전트로 확장(빌더≠검증자, 검증자 모델 ≥ 빌더 모델 — [[techniques.orchestrator-model-routing]]).

## 3캠페인 구현 형태
- **canvas**: 이 루프를 문서로 명문화한 원 출처(`parity-rep-method.md`). ⑤검증은 `_bN_verify.py` 스위트([[techniques.regression-harness-suite]])가 담당.
- **notion**: ①②를 `ci_agent.py`+`ci_compare.py`가 실물·클론 동시 실행으로 자동화, ⑤검증은 다양한 `*_gate.py`.
- **akiflow**: ⑤검증을 `gate.py` 하나로 통합해 "parity 24/24 · flow 56/56 · glyph mismatch 0"을 한 번에 리포트하는 형태로 진화.

## 로깅 규율
루프의 매 사이클이 [[techniques.append-only-logging]] 원칙으로 워크로그에 기록되어야 다음 세션(특히 무인 야간 런)이 어디까지 왔는지 신뢰하고 이어갈 수 있다.

## 관련
- [[pipelines.night-run]] — 이 루프를 사람 없이 밤새 반복시키는 상위 운영 SOP
