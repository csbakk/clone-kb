---
id: techniques.orchestrator-model-routing
title: 오케스트레이터 모델 라우팅 (fable 오케 / sonnet 빌더 / opus 검증)
doctype: technique
status: standard
proven_in: [canvas]
related: [techniques.adversarial-verification, techniques.subagent-fanout-rules, techniques.night-run-sop]
evidence:
  - "260615_canvas-clone/docs/2026-07-11-parity-rep-method.md §3 mermaid — SA['verify-first 서브에이전트<br/>빌더(sonnet) ≠ 검증자(opus/fable)']"
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md GATE1 라벨 — '적대 검증 게이트(opus, 자가선언 불신)'"
  - "260615_canvas-clone/ref/_VERIFY_r1.md L3 — '검증자 = 독립 적대적 에이전트'"
updated: 2026-07-13
owner: 박춘순
---

# 오케스트레이터 모델 라우팅 (fable 오케 / sonnet 빌더 / opus 검증)

**한 줄**: 역할마다 다른 모델 티어를 배정한다 — 오케스트레이터(계획/감독)=fable, 빌더(구현)=sonnet, 검증자(적대적 재측정)=opus/fable. **검증자 티어는 항상 빌더 이상**이어야 한다.

## 확인된 근거 (중요: 정직하게 표기)
canvas-clone 캠페인 문서에서 **빌더=sonnet, 검증자=opus/fable**, "검증자 모델 ≥ 빌더 모델"이라는 불변식은 명시적으로 확인됨(위 evidence). 반면 clone-campaign-kit(NIGHT-RUN.md, PARITY-LOOP.md)은 오케스트레이터/dev 서브에이전트/verify 서브에이전트라는 **역할 분리**는 명시하지만, 이 역할들에 구체적으로 어떤 Claude 모델(fable/sonnet/opus)을 배정하라는 문장은 kit 텍스트 자체에서는 확인되지 않았다 — kit은 역할 분리까지만 일반화되어 있고, 모델 배정은 canvas 캠페인에서만 명문화된 상태다. 다른 캠페인으로 이 라우팅을 이식할 때는 "검증자 ≥ 빌더" 원칙만 확실히 가져가고, 구체 모델명은 그때그때 가용 모델에 맞춰 재확인할 것.

## 왜 이렇게 나누나
- 오케스트레이터: 큐 관리·진행 판단·산출물 확인(디스크 기준) — 넓은 컨텍스트, 빠른 판단이 중요. 창작보다 감독.
- 빌더: 실제 코드/스크립트 작성 — 물량이 많으므로 비용 효율적인 티어.
- 검증자: 빌더의 자가선언을 불신하고 재측정 — 빌더와 같은 맹점을 공유하면 안 되므로 **더 높은(혹은 최소 동급) 티어**를 배정해 판단력 격차를 만든다.

## 관련
- [[techniques.adversarial-verification]] — 이 라우팅이 가능하게 하는 검증 방식
- [[techniques.subagent-fanout-rules]] — 병렬 서브에이전트 배치 시 같이 고려하는 규칙
