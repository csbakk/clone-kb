---
id: techniques.visual-triage-sheet
title: G1 비주얼 판정 시트 (bbox 오버레이 + 크롭)
doctype: technique
status: experimental
proven_in: [notion]
related: [techniques.rip-repair-loop, techniques.rip-css-dump, techniques.dom-first-measurement]
evidence:
  - "260622_notion-clone/harness/rip_repair.py `visual` 서브커맨드 + harness/test_triage_visual.py (4검증 PASS)"
  - "260622_notion-clone/ref/rip/repair_view_gallery_triage_visual.md — G1 17건 첫 실전 시트"
updated: 2026-07-13
owner: 박춘순
---

# G1 비주얼 판정 시트 (bbox 오버레이 + 크롭)

**한 줄**: 수복 triage가 "사람 판단 필요(G1)"로 넘긴 델타를 사람이 실제로 판단할 수 있게, 클론 실캡처와 실물 덤프 와이어프레임 위에 G1 항목을 번호 박스로 오버레이하고 항목별 크롭+정체 설명+판단 선택지를 붙인 시트를 자동 생성한다.

## 왜 (탄생 배경 — 사용자 피드백 직결)
notion RUN4에서 triage G1 17건이 bbox/path 텍스트로만 나열되자 오너가 "시각 요소 없이 텍스트로는 판단 불가"라고 보고. **G1의 존재 이유가 '사람 판단'인데 판단 재료가 사람이 못 읽는 형식인 구조적 모순** — 판단을 요구하는 모든 자동화는 판단 가능한 형식으로 증거를 내야 한다.

## 어떻게
1. triage 리포트에서 G1 항목(bbox·path·kind) 파싱, 최신 덤프 JSON으로 좌표 재조회.
2. **클론**: CDP로 상태 재현 후 실캡처 → G1 bbox 빨간 박스+번호 오버레이 (G2/G3는 기본 제외 — 소음 방지).
3. **실물**: 비파괴 원칙 유지 — 접속하지 않고 real 덤프 JSON에서 **와이어프레임 렌더**(전 노드 회색 박스+텍스트 라벨, 한글은 시스템 폰트 로드). 기캡처 스크린샷이 있으면 그걸 사용.
4. 항목별 bbox ±40px 크롭 + **정체 한 줄 설명**(clone은 cls로 정확 판별, real은 role/text/부모경로 패턴) + 판단 선택지("클론에서 제거 / 실물대로 구현 / 예외 등록").
5. md 시트에 이미지 상대경로 임베드(Obsidian/VSCode 렌더) → 오너는 시트만 보고 결정.
6. 게이트: G1 전원이 오버레이에 포함·임베드 경로 실재를 코드로 검증 + 오버레이를 에이전트가 직접 이미지로 열어 눈검증.

## 결과 (notion 파일럿)
- view_gallery G1 17건 → 4클러스터로 즉시 판독 가능: 실물 커버 wrapper(1/4)·호버 액션쌍(2/3/5)·대형 add-tile(6/7) vs 클론 열기버튼(8/11/14)·속성칩(9/12/15)·날짜메타(10/13/16)·새로만들기(17).
- 오너 판단 대기 시간이 "덤프 재해석 세션 1회"에서 "시트 1장 열람"으로 단축.

## 함정
- 실물 와이어프레임은 색·이미지·폰트가 없다 — "존재/위치/텍스트" 판단엔 충분하나 스타일 판단엔 부족. 스타일 G1이 많으면 사용자 입회 세션에서 실물 스크린샷 확보 후 재생성.
- 오버레이 좌표는 dpr=1 전제 — retina 캡처면 좌표 변환 필요([[techniques.pixel-screenshot-as-primary-oracle]] 은퇴 사유였던 드리프트 주의).

## 관련
- [[techniques.rip-repair-loop]] — 이 시트가 G1 병목을 푸는 후속 단계
- [[techniques.dom-first-measurement]] — "측정은 DOM, 사람 판단 증거는 픽셀" 역할 분담
