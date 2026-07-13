---
id: cases.canvas
title: 캠페인 사례 — Higgsfield Canvas 클론 (260615_canvas-clone)
doctype: case
status: verified
proven_in: [canvas]
related: [pipelines.rip-v1, pipelines.99-percent, pipelines.verify-first-loop, techniques.dogfooding-as-bug-discovery]
evidence:
  - "~/Documents/project/260615_canvas-clone/ (외부 경로, 이 KB는 포인터만 보유)"
updated: 2026-07-13
owner: 박춘순
---

# 캠페인 사례 — Higgsfield Canvas 클론

**외부 작업폴더**: `~/Documents/project/260615_canvas-clone/` (실물 앱: Higgsfield Canvas, 노드캔버스형 생성 AI 툴)

## 현재 상태 (2026-07-13 기준)
- **dev 서버**: `localhost:5175` (`npm run dev`) · **CDP 포트**: 9223, 프로필 `~/.chrome-canvas-clone`
- **파리티 게이트**: 8종 통과 (셸·노드·인터랙션·모델/업로드·상태/서피스/도구·크롤러)
- **RIP 레이어① 상태**: 19/19 전수 덤프, 0 스킵. attribute-diff 38,476 → 30,580 (**-20.5%**, 글로벌 CSS 리셋 배치 1회 후)
- **테스트**: `npx vitest run` — 37/37, 상시 GitHub Actions CI
- **브랜치**: `polish-effects`(구 데모 레이어, 2026-07-13 철거) vs `parity`(활성 캠페인 브랜치)

## 이 캠페인이 낳은 기법
- [[techniques.rip-css-dump]] · [[techniques.rip-crawler]] · [[techniques.rip-repair-loop]] — RIP 3단 파이프라인 원류 ([[pipelines.rip-v1]])
- [[techniques.cdp-raw-driver]] — 좀비 탭 우회 (cdp_raw.py)
- [[techniques.model-matrix-diff]] — 66개 모델 카탈로그 전수 검증, GENERATE 비용 0
- [[techniques.dogfooding-as-bug-discovery]] — BORI 사례, 실사용 4회 실생성으로 6개 실버그 발견·수정
- [[techniques.url-escape-guard]] — 크롤러가 실제로 유발한 네비게이션 사고에서 신설
- [[techniques.orchestrator-model-routing]] — 빌더(sonnet)≠검증자(opus/fable) 규칙의 원 출처
- [[pipelines.99-percent]] — 6축 판정식 정의 원 출처

## 잔여 티켓 / 남은 일
- RIP 잔여 델타: 커서 불일치(740), fontWeight(620), 색상 근사(#fff↔#f7f7f8, ~3,400), display/position(~1,600) — 시스템 토큰으로 안 잡히는 컴포넌트별 케이스워크로 분류.
- 모델피커 Featured 카피 시각 diff — T-E 원 범위, 아직 미해결.
- 크롤러 상태 커버리지 확장.
- 99% 판정식 P1(cross-paste)~P4(pixel-fingerprint) 전부 미착수 — [[pipelines.99-percent]] 참고.
- 커스터마이징 트랙(Comfy 노드, live LLM planner)은 `src/live/`에 보존만 된 채 미배선.

## 최근 세션
2026-07-13 (RIP-T-E 배치, `--radius-btn`/`--radius-pill` 토큰 분리 마무리).
