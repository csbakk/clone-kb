---
id: techniques.model-matrix-diff
title: 모델 매트릭스 diff (카탈로그 전수 검증, GENERATE 비용 0)
doctype: technique
status: verified
proven_in: [canvas]
related: [techniques.regression-harness-suite, techniques.cdp-nondestructive-recon]
evidence:
  - "260615_canvas-clone/harness/model_matrix_diff.py — window.__loadDoc 훅으로 카탈로그 매핑 전 모델 노드 스폰, .hf-field/handle 덤프, ref/model_matrix/*.json과 diff"
  - "REC-D 정찰: 66개 모델(비디오27+이미지21+오디오4+LLM5+어시스턴트1), 30개 게이팅 그룹 카탈로그"
  - "260615_canvas-clone 세션18(2026-07-16) — registry 표시비용이 실측과 어긋남 발견(seedance 표시 18cr vs 실측 17.5cr, 경미하나 부정확)"
  - "260615_canvas-clone 세션19(2026-07-16) — KLING v3.0 실단가를 MCP 거래내역으로 확정(12.5cr/클립), registry 표시값보다 정확·seedance(17.5cr)보다 저렴함을 실측. ★크레딧 비교·모델 선택 판단은 registry 표시값이 아니라 MCP balance/transactions 기준으로만 한다는 원칙 재확인"
updated: 2026-07-16
owner: 박춘순
---

# 모델 매트릭스 diff (카탈로그 전수 검증, GENERATE 비용 0)

**한 줄**: 생성형 AI 캔버스 앱에서 "모델을 66개 다 골라보면서 인스펙터 필드가 실물과 맞는지" 확인하는 건 사람이 하면 지루하고 실수하기 쉽다. 개발자 훅으로 노드를 스폰만 시키고(실제 GENERATE는 안 함) 필드 구성을 덤프해 기준 JSON과 diff한다.

## 어떻게 (harness/model_matrix_diff.py)
1. 카탈로그에 매핑된 모든 모델(subtype+modelId 조합)에 대해 개발자 훅 `window.__loadDoc`으로 제너레이트 노드를 스폰 — **실제 GENERATE 클릭 없음, 비용 0**.
2. 각 노드의 인스펙터를 `hf:toggle-inspector` 이벤트로 열고 `.hf-field` 로우(라벨+컨트롤 종류)와 `.react-flow__handle[data-handlepos=left]`(입력 핸들)를 덤프.
3. `ref/model_matrix/*.json`(REC-D 정찰로 만든 66개 모델 기준 데이터: 비디오27+이미지21+오디오4+LLM5+어시스턴트1, 게이팅 그룹 30개)과 diff.
4. `python3 harness/model_matrix_diff.py [--json out.json]` — `✅ 전 모델 불일치 0` 또는 `⚠ N개 모델 불일치` 출력.

## 왜 중요한가
- 모델마다 인스펙터 필드 구성(파라미터 종류, 게이팅 규칙)이 달라 수동 검증은 66회 반복 작업 — 자동화 없인 사람이 절대 안 함(=검증 공백으로 방치됨).
- 클론 전용, 실물 탭 접근 불필요 — 크롤러/정찰과 달리 실물을 전혀 안 건드리므로 안전 부담이 없음.

## 함정
- 이 기법은 "필드 구성이 맞는지"만 검증한다 — 실제 생성 결과물의 품질/정확도는 별도 검증 필요(→ [[techniques.dogfooding-as-bug-discovery]]처럼 실사용으로 잡아야 하는 영역).
- ★**registry에 표시되는 비용(cr)이 실제 청구액과 다를 수 있다** (canvas 세션18~19). 표시값을 카탈로그 정합의 일부로만 diff하고, 실제 비용 판단(모델 선택·예산 산정)은 반드시 MCP `balance`/`transactions`로 확정한다 — 빌더의 표시값 추정이나 bridge-history 추정은 세션18에서 ~70cr급 오산을 낸 전례가 있음(크로스캠페인 결정: PROTOCOL.md §2.5 "크레딧 정본 = MCP 거래내역").
- 모델별 지원 파라미터(예: 종횡비)가 일부 모델에서 사전 고지 없이 제한될 수 있다 — canvas 세션19에서 KLING 3.0이 4:5 비율을 지원하지 않아 생성 시도 실패로만 드러남(AD4는 비디오만 9:16 예외 처리). 아직 이 매트릭스는 `model_matrix_diff.py` 기준 JSON에 편입되지 않음(이월 과제).

## 관련
- [[techniques.regression-harness-suite]] — 이 스크립트가 속하는 상위 검증 스위트 패턴
