---
id: techniques.cross-paste-parity
title: 크로스-페이스트 파리티 (라운드트립 diff 0)
doctype: technique
status: verified
proven_in: [canvas]
related: [techniques.clipboard-source-of-truth, pipelines.99-percent]
evidence:
  - "260615_canvas-clone ref/_XPASTE_ROUNDTRIP_r1.md (2026-07-13) — P1 파일럿: 실물→클론 5/5 타입 diff 0·클론→실물 수용 4/4·왕복 4/4 diff 0(기준 '3타입+' 초과)·클론 내부 왕복 5/5"
  - "260615_canvas-clone ref/_VERIFY_r1.md §Z — opus 적대검증 4렌즈 통과, 승격 기준 충족(MET)·신규 결함 0"
updated: 2026-07-13
owner: 박춘순
---

# 크로스-페이스트 파리티 (라운드트립 diff 0)

**한 줄**: 클론이 실물의 클립보드 직렬화 계약을 그대로 채택해, 실물↔클론 어느 방향으로 붙여넣어도 정규화 diff 0이 되는 것을 자동 게이트로 삼는 기법 — [[techniques.clipboard-source-of-truth]](정찰 원칙)의 구현+게이트 확장.

## 실행 절차 (canvas P1에서 검증된 형태)
1. **규격 재실측**: 노드 타입별 Cmd+C 캡처 + paste 의미론(id 재매핑·position 규칙·엣지 복원·stale 처리)까지. 과거 정찰을 믿지 말고 재실측 — canvas에서 핵심 가정(클립보드에 JSON 직접)이 뒤집혔다(실제=마커+localStorage 2단 구조).
2. **어댑터**: 클론 내부 포맷 ↔ 실물 페이로드 양방향 순수함수 + 실측 JSON을 vitest 픽스처로 직접 사용.
3. **배선**: Cmd+C/V를 실물 규격으로 교체. paste 의미론(재매핑·위치·quirk)을 실측대로 — 실물의 버그성 quirk(예: results[].node_id 재매핑 누락)까지 의도적 재현.
4. **라운드트립 검증**: 실물→클론 재현 / 클론→실물 수용 / 왕복 diff 0. diff는 실측으로 정의된 **정규화 규칙**(id=정합성 비교, 실물이 버리는 필드=제외)로 스크립트 판정 — 규칙 밖 차이는 전부 결함.
5. **적대 검증**: 빌더의 diff 스크립트를 불신하고 독립 비교 로직으로 재측정.

## 함정 (canvas 실측)
- **paste 트리거 비대칭**: 실물은 CDP 합성 Cmd+V에 무반응(copy는 됨) — OS 레벨 `key code 9` 필요. 클론엔 게이트가 없어 CDP로 충분. 자동화 설계 시 앱마다 실측할 것.
- 정규화 규칙이 결함을 숨기지 않는지(제외 필드마다 실측 근거) 적대 검증 렌즈로 감사.
- 단일 노드 픽스처만으로는 다중노드+엣지 왕복이 미검증으로 남는다 — 케이스 설계 시 명시적으로 포함(canvas 잔여 티켓).

## 관련
- [[techniques.clipboard-source-of-truth]] — 기반 정찰 원칙(경계: 그 카드=추출 정본, 이 카드=구현+게이트)
- [[pipelines.99-percent]] — 판정식 항목④ (canvas P1로 달성)
