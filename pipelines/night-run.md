---
id: pipelines.night-run
title: 야간 무인 런 파이프라인
doctype: pipeline
status: standard
proven_in: [kit, notion, akiflow]
related: [techniques.night-run-sop, techniques.port-profile-isolation, techniques.append-only-logging, techniques.subagent-fanout-rules, pipelines.verify-first-loop]
evidence:
  - "clone-campaign-kit/NIGHT-RUN.md"
  - "260622_notion-clone/ref/_AUTONOMOUS_10H_0712_RUN2.md, _AUTONOMOUS_10H_0713_RUN3.md — 실제 10시간 무인 런 2회"
  - "260622_akiflow-clone/_ORCH_KICKOFF.md — cmux 기반 오케스트레이터 킥오프"
updated: 2026-07-13
owner: 박춘순
---

# 야간 무인 런 파이프라인

**한 줄**: [[pipelines.verify-first-loop]]를 사람 없이 밤새 반복시키기 위한 상위 조립 — 격리·로깅·병렬화·안전경계 4개 기법을 하나의 운영 SOP로 묶는다.

## 조립도

```mermaid
flowchart TB
    subgraph PRE["사람 10~15분 (자기 전)"]
        Q["_TICKETS.md 우선순위 정리"]
    end
    subgraph NIGHT["AI 무인 밤새"]
        direction LR
        L["verify-first-loop<br/>반복 실행"] --> ISO["port-profile-isolation<br/>Chrome 1워커 직렬화"]
        ISO --> FAN["subagent-fanout-rules<br/>독립·무충돌만 병렬"]
        FAN --> LOG["append-only-logging<br/>_WORKLOG/_BLOCKED 기록"]
        LOG -->|막힘| SKIP["graceful skip<br/>_BLOCKED.md 기록 후 다음 티켓"]
        LOG -->|통과| L
        SKIP --> L
    end
    subgraph POST["사람 5분 (아침)"]
        R["_BLOCKED.md + 커밋 로그만 확인"]
    end
    PRE --> NIGHT --> POST

    classDef human fill:#fff3cd,stroke:#b8860b,stroke-width:2px;
    classDef ai fill:#d1e7ff,stroke:#1c64c2,stroke-width:2px;
    class Q,R human;
    class L,ISO,FAN,LOG,SKIP ai;
```

## 핵심 불변식 ([[techniques.night-run-sop]]에서 상속)
완료 판단은 디스크 산출물로만(워커 자가보고 불신), 막힘 카운트 초과 시 부분결과 저장 후 정지, 무맹목 삭제·실데이터 mutation·포커스 스틸(`bringToFront`) 금지.

## 실적
- notion-clone: 10시간 무인 런 2회(RUN2, RUN3) — RIP 구조 델타 30%↓.
- akiflow-clone: cmux 기반 무인 오케스트레이터가 이 파이프라인을 그대로 채택해 킥오프.

## 관련
- [[pipelines.verify-first-loop]] — 이 파이프라인이 반복시키는 작업 단위
- [[techniques.orchestrator-model-routing]] — 무인 런의 오케스트레이터/빌더/검증자 모델 배정(canvas 한정 실증, 다른 캠페인은 역할분리까지만 확인됨)
