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
updated: 2026-07-13
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

## 관련
- [[techniques.regression-harness-suite]] — 이 스크립트가 속하는 상위 검증 스위트 패턴
