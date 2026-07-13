---
id: techniques.dogfooding-as-bug-discovery
title: 실사용(dogfooding)으로 버그 발견 — BORI 사례
doctype: technique
status: verified
proven_in: [canvas]
related: [techniques.regression-harness-suite, techniques.model-matrix-diff]
evidence:
  - "260615_canvas-clone/ref/_DOGFOOD_BORI.md (2026-07-12) — 실제 12컷 스토리보드 중 4컷 크롭→업로드→노드연결→Kling 3.0 실생성 4/4 성공, 6개 실버그 발견·수정"
updated: 2026-07-13
owner: 박춘순
---

# 실사용(dogfooding)으로 버그 발견 — BORI 사례

**한 줄**: 검증 스크립트가 아무리 촘촘해도 "진짜 작업을 진짜로 해보는" 것만이 잡아내는 버그 클래스가 있다. 실제 크레딧을 쓰는 실생성까지 포함한 진짜 작업을 한 번 통째로 해본다.

## 사례 (2026-07-12, 사용자 승인 하에 진행)
스토리보드 이미지(`05_storyboard_A.png`, 12컷)에서 4컷을 PIL 휘도 프로파일 엣지검출로 정밀 크롭 → 클론 UI로 업로드 → 미디어를 VideoGenerator 노드에 연결 → Kling 3.0 선택 → 4회 실생성(실제 크레딧 소모) → ffprobe로 4/4 성공 검증(진짜 3.04초 mp4, 플레이스홀더 아님).

## 발견된 6개 실버그 (전부 당일 근본원인 규명·수정)
1. **업로드 이미지 깨짐**: `<img>`에 `onError` 핸들러가 없어 브라우저 로드-실패 레이스가 재시도 없이 방치됨 → `RetryImage` 컴포넌트 신설(key-remount 방식 1회 자동 재시도).
2. **비용 배지 고정값**: 인스펙터/툴바/멀티셀렉트바 3곳에 각각 다른 비용 계산이 흩어져 있어 모델 변경 시 일부만 갱신 → `src/data/generate.ts`에 `estimatedCost()` 단일 함수로 통합.
3. **모델칩 클릭 오동작**: 옆 노드의 이미 열려있던 피커의 백드롭-닫기 버튼이 `display:none`이라 시각적으로 다음 노드의 칩을 덮으며 클릭을 가로챔 — 하네스 재현 스크립트로 근본원인 특정.
4. **표시비용≠실제청구**(7.5 vs 3.75): 정적 비용이 6초 기준 추정치인데 사용자가 3초로 설정 — `estimatedCost()`를 duration 비율로 스케일링해 수정.
5. **데이터 유실(최고 심각도)**: 캔버스가 작업 중 조용히 stale localStorage 스냅샷으로 리셋되며 방금 만든 노드 5개 소실. 최초 의심(Escape 키)은 틀렸음 — `CanvasApp.tsx` 전수 감사로 진짜 원인 특정: 마운트 시 localStorage 하이드레이션이 전혀 없고, `persistCurrentDoc()`이 폴더 이동/뒤로가기에만 트리거되어 일반 편집에는 저장이 전혀 안 됨. 마운트 시 하이드레이션 + 600ms 디바운스 자동저장으로 수정, 실사용 재현으로 검증(노드 2개 생성→Escape 8회→1초 대기→강제새로고침→노드 복원 확인, 수정 전엔 100% 유실).
6. **Sound 토글 클릭이 인스펙터 전체를 닫음**: 인스펙터 위치 clamp가 뷰포트 상단만 clamp하고 하단은 안 해서, 화면 하단 근처 노드에서는 Sound 로우가 화면 밖으로 밀려나 클릭이 캔버스 패널에 떨어짐(바깥클릭 핸들러가 "정상 동작"한 것 — 잘못된 기하가 원인) → `clampBottom` 콜백 ref로 수정.

## 재검증
전 수정 후 vitest 36/36, 클린 빌드, `_b1/_b3/_b5/_b8_verify.py` 전부 통과(콘솔 에러 0).

## 왜 중요한가
6개 버그 중 특히 5번(데이터 유실)은 규모가 크고 어떤 자동 크롤러/검증 스위트도 우연히 잡기 어려운 조건(마운트-후 시간 경과 + 특정 네비게이션 패턴)에서만 드러났다 — "진짜 작업을 진짜로 해본다"만이 잡는 버그 클래스가 실존함을 실증.

## 함정
- 실제 크레딧/비용이 드는 액션이므로 **사용자 승인 필수**, 무인 야간 런의 기본 동작으로 자동화하면 안 됨([[techniques.night-run-sop]]의 "실데이터 mutation 금지"와 상충하지 않도록 항상 사람이 트리거).

## 관련
- [[techniques.regression-harness-suite]] — 이 사례로 발견된 버그들이 회귀 스위트에 편입됨(`_b1/_b3/_b5/_b8_verify.py`)
