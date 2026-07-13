---
id: techniques.adversarial-verification
title: 적대적 검증 (빌더 ≠ 검증자, verify-first 루프)
doctype: technique
status: standard
proven_in: [canvas, notion]
related: [techniques.orchestrator-model-routing, techniques.regression-harness-suite, techniques.record-during-hover, pipelines.verify-first-loop]
evidence:
  - "260615_canvas-clone/docs/2026-07-11-parity-rep-method.md §3 — 'verify-first 서브에이전트(빌더≠검증자, 검증자 모델 ≥ 빌더 모델)'"
  - "260615_canvas-clone/ref/_VERIFY_r1.md L3 — '검증자 = 독립 적대적 에이전트. 빌더 자가선언을 불신하고 처음부터 재측정'"
  - "260622_notion-clone/harness/ci_agent.py + ci_compare.py — 동일 제스처를 실물/클론 두 탭에서 동시 실행해 8개 시그널 정규식으로 DOM 변이 diff"
updated: 2026-07-13
owner: 박춘순
---

# 적대적 검증 (빌더 ≠ 검증자, verify-first 루프)

**한 줄**: "완료했다"는 빌더의 자가선언을 신뢰하지 않는다. 별도 주체(스크립트든 다른 모델이든)가 처음부터 다시 측정해서 통과/실패를 판정한다.

## 언제 쓰나
게이트/티켓을 "완료"로 표시하기 직전. 특히 무인 야간 런에서는 빌더 self-report만으로 완료 판정을 내리면 안 됨 (→ [[techniques.night-run-sop]]의 "디스크 산출물로만 완료 판단" 규칙과 동일 뿌리).

## 두 가지 구현 형태 (실증됨)
1. **모델 계층 분리** (canvas) — 빌더=sonnet, 검증자=opus/fable. `99-percent-plan.md` GATE1 라벨: "적대 검증 게이트(opus, 자가선언 불신)". 검증자 모델 티어가 빌더보다 낮으면 안 된다는 명시적 불변식.
2. **동일 오라클 이중 실행** (notion) — `ci_agent.py`가 Clone Inspector 확장을 CDP로 구동해 실물 탭·클론 탭에 **같은 제스처**(예: 블록 0 클릭 후 3까지 shift-click)를 동시에 흘리고, `ci_compare.py`가 두 DOM 변이 로그를 8개 시그널 정규식(halo/overlay, `position:relative`, 노션 블루 `rgba(35,131,226,...)`, opacity, transform, `display:none`, `class=selected`)으로 대조 — "REF만/CLONE만 발생"을 자동 출력. 이건 별도 AI 역할 분리는 아니지만 "같은 입력, 두 개의 독립 오라클" 원칙은 동일.

## 왜 필요한가
빌더 에이전트는 구조적으로 자기 작업을 낙관적으로 보고하는 편향이 있다 (canvas 사례: "G1~G16 완료·수치 일치" 자가선언을 검증자가 재측정해서 반례를 찾은 이력 다수). 검증자가 빌더와 같은 모델/같은 컨텍스트면 같은 맹점을 공유해 통과시켜버릴 위험이 있다.

## 함정
- 검증자가 "빌더 코드를 읽고 판단"만 하면 약해진다 — 반드시 **처음부터 재측정**(스크립트 재실행 or 별도 캡처)해야 함.
- 검증자 모델을 빌더보다 낮은 티어로 배정하면 이 기법의 전제가 무너진다.

## 관련
- [[techniques.orchestrator-model-routing]] — 이 기법을 가능하게 하는 모델 배정 규칙
- [[pipelines.verify-first-loop]] — 이 기법이 들어가는 상위 루프
