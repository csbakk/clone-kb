---
id: techniques.clipboard-source-of-truth
title: 클립보드 JSON을 정본으로 (노드캔버스 앱)
doctype: technique
status: standard
proven_in: [canvas]
related: [techniques.cross-paste-parity, techniques.dom-first-measurement]
evidence:
  - "__obsidian/wiki/concepts/노드캔버스앱-복제-실전기법.md (2026-06-09) — Cmd+C→OS클립보드 JSON({nodes,edges})이 DOM/React-fiber 파싱보다 정확, 적용 사례 _tmp/hf_canvas_학습/"
  - "260615_canvas-clone/docs/2026-07-11-parity-campaign-strategy.md §4-② — '노드 데이터: 실물 노드 선택→Cmd+C 클립보드 JSON(정본). DOM 파싱·fiber보다 정확. stale 함정 → id·타입 교차검증'"
updated: 2026-07-13
owner: 박춘순
---

# 클립보드 JSON을 정본으로 (노드캔버스 앱)

**한 줄**: React Flow류 노드캔버스 앱에서 노드/엣지 데이터의 정본은 DOM이 아니라 **Cmd+C가 OS 클립보드에 쓰는 JSON**(`{nodes, edges}`)이다.

## 언제 쓰나
Higgsfield Canvas 같은 노드캔버스 앱을 클론할 때 노드 스키마(필드명, 타입, 좌표계)를 파악해야 하는 모든 순간. React DevTools로 fiber를 파싱하는 것보다 이 방법이 항상 더 정확하고 빠르다.

## 왜 DOM/fiber보다 나은가
- DOM은 렌더링 결과일 뿐 — 가상화(virtualization)로 화면 밖 노드가 언마운트되거나, 스타일 계산 과정에서 원본 데이터 구조가 소실된다.
- React fiber 파싱은 내부 구현에 강하게 결합되어 리액트 버전/빌드마다 깨지기 쉽다.
- Cmd+C가 만드는 클립보드 JSON은 **앱이 스스로 선언한 직렬화 계약**이다 — 실물 앱 개발자가 "이게 내 노드 데이터의 진짜 모양"이라고 보증하는 것과 같다.

## 어떻게
1. 실물 캔버스에서 노드(들)를 선택 → Cmd+C.
2. OS 클립보드를 읽어 JSON 파싱 (`{nodes:[...], edges:[...]}` 형태 확인).
3. 클론 쪽에서 같은 스키마로 노드를 만들 수 있는지 대조.

## 함정
- **stale 클립보드 함정**: 이전에 복사해둔 JSON이 남아있는데 다른 노드를 다시 복사했다고 착각하기 쉽다 → 매번 id·타입 필드를 교차검증해서 "지금 막 복사한 게 맞는지" 확인.
- 붙여넣기(paste)로 노드를 복원할 때 **엣지가 유실**되는 경우가 있었다 (노드만 복원, 엣지 드롭) — 노드 데이터 자체는 신뢰해도 라운드트립(복사→붙여넣기) 자동화는 별도 검증이 필요 → [[techniques.cross-paste-parity]] (실험적, 아직 자동화 미완).

## 관련
- [[techniques.cross-paste-parity]] — 이 원칙을 "라운드트립 diff 0" 자동 게이트로 확장하려는 실험적 후속 기법 (canvas 99% 로드맵 P1, 2026-07-13 기준 설계만 되고 미실행)
