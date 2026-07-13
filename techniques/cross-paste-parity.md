---
id: techniques.cross-paste-parity
title: 크로스-페이스트 파리티 (라운드트립 diff 0)
doctype: technique
status: experimental
proven_in: []
related: [techniques.clipboard-source-of-truth, pipelines.99-percent]
evidence:
  - "260615_canvas-clone/docs/2026-07-13-99-percent-plan.md §3-A, §6 — 판정식 항목④, 파일럿 기준: '실물→클론 paste 재현 + 라운드트립 diff 0(노드 3타입 이상)'. 어댑터 src/data/hfClipboard.ts 계획만, 2026-07-13 기준 미착수"
updated: 2026-07-13
owner: 박춘순
---

# 크로스-페이스트 파리티 (라운드트립 diff 0)

**한 줄**: 실물에서 Cmd+C한 노드를 클론에 붙여넣었을 때 완전히 같은 결과가 나오는지(라운드트립 diff 0) 자동 게이트로 만들려는 계획 — [[techniques.clipboard-source-of-truth]]의 자동화 확장판.

## 상태: 설계만 됨, 미실행
canvas 99% 로드맵의 P1 항목. "실물→클론 paste 재현 + 라운드트립 diff 0(노드 3타입 이상)"이 파일럿 통과 기준으로 정의되어 있으나, 2026-07-13 기준 어댑터(`src/data/hfClipboard.ts`)조차 아직 작성 전 — **아이디어와 판정 기준만 문서화된 단계**.

## 왜 experimental인가
[[techniques.clipboard-source-of-truth]]는 "사람이 손으로 클립보드 JSON을 읽어 정본으로 삼는다"는 부분까지는 실증됐지만, "붙여넣기 자동화 + 라운드트립 diff를 게이트로 자동 판정"까지는 아직 스크립트도, 실행 기록도 없다. 승격하려면 최소 1회 실제 파일럿 실행과 수치(diff 0 확인)가 필요.

## 관련
- [[techniques.clipboard-source-of-truth]] — 이 기법의 기반이 되는 이미 검증된 원칙
- [[pipelines.99-percent]] — 이 기법이 속한 6축 판정식의 항목④
