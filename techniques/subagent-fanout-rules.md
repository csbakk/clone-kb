---
id: techniques.subagent-fanout-rules
title: 서브에이전트 병렬화 규칙 (독립·무충돌만 병렬)
doctype: technique
status: standard
proven_in: [kit, canvas, notion]
related: [techniques.orchestrator-model-routing, techniques.night-run-sop, techniques.adversarial-verification]
evidence:
  - "clone-campaign-kit/knowledge/야간-무인-복제-시스템.md §6.4 — 5조 규칙(독립+무충돌만 병렬, 공유파일은 메인만 편집, 결정적 작업=스크립트, 판단필요=에이전트, 순차의존=메인직접)"
  - "260615_canvas-clone/docs/2026-07-11-parity-rep-method.md §3 — 갭이 티켓화되어 병렬 여지가 생기면 verify-first 서브에이전트로 확장"
  - "__obsidian/wiki/concepts/웹앱-클론-캠페인-운영.md §5 — 'notion-clone M4 DB 6뷰에서 실증 — 한 번에 6뷰 동시 구현'"
updated: 2026-07-13
owner: 박춘순
---

# 서브에이전트 병렬화 규칙 (독립·무충돌만 병렬)

**한 줄**: "병렬 가능(독립·무충돌) + 판단/생성이 필요" 한 경우에만 서브에이전트를 병렬로 띄운다. 단일·순차의존·결정적 계산은 메인 세션이나 스크립트로 직접 처리한다.

## 5조 규칙 (kit 정본)
1. 독립 작업, 2개 이상, 파일 충돌 없음(자기 파일 + 전용 CSS만 건드림) → ✅ 병렬 `component-builder`.
2. 공유 파일(components.css/store/types) 건드릴 때 → 서브에이전트는 읽기/분석만 병렬, **편집은 메인만**.
3. 결정적 작업(수치 diff, 빌드, 측정) → 에이전트 말고 **스크립트**.
4. 판단이 필요한 작업(비주얼 갭, 디자인 선택) → 에이전트.
5. 단일/순차의존 작업 → 메인이 직접.

한 줄 요약: "병렬 가능(독립·무충돌) + 판단/생성 필요 → 서브. 단일·순차·결정적 → 메인/스크립트."

## 실증 사례
- **notion M4**: DB 6개 뷰(테이블/보드/캘린더/갤러리/타임라인/리스트)를 한 번에 서브에이전트 6개로 동시 구현 — 서로 다른 파일, 충돌 없음, 판단(각 뷰의 렌더 로직)이 필요한 전형적 케이스.
- **canvas**: 갭이 티켓 단위로 쪼개진 뒤에야 verify-first 서브에이전트로 병렬 확장 — 티켓화 이전(갭매트릭스 원시 상태)에는 메인 세션이 직접 처리.

## 왜 이 규칙이 필요한가
- 결정적 계산(예: 픽셀 diff 수치)을 에이전트에게 맡기면 부정확하고 토큰 낭비 — "결정적인 건 코드"(kit 정본 문구).
- 공유 파일을 여러 서브에이전트가 동시에 건드리면 머지 충돌·레이스 컨디션 발생 — atomic-localstorage-inject 기법이 이 문제를 별도로 다룸 (localStorage 버전, → [[techniques.atomic-localstorage-inject]]).

## 함정
- "병렬화하면 빠르다"는 유혹에 공유 상태 파일까지 병렬로 건드리게 하면 오히려 정리 비용이 더 든다.

## 관련
- [[techniques.orchestrator-model-routing]] — 병렬 배치되는 서브에이전트들의 모델 티어 배정 규칙
