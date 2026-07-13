---
id: cases.akiflow
title: 캠페인 사례 — Akiflow 클론 (260622_akiflow-clone)
doctype: case
status: verified
proven_in: [akiflow]
related: [pipelines.verify-first-loop, pipelines.night-run, techniques.port-profile-isolation, techniques.regression-harness-suite]
evidence:
  - "~/Documents/project/260622_akiflow-clone/ (외부 경로, 이 KB는 포인터만 보유)"
updated: 2026-07-13
owner: 박춘순
---

# 캠페인 사례 — Akiflow 클론

**외부 작업폴더**: `~/Documents/project/260622_akiflow-clone/` (실물 앱: Akiflow, 태스크/캘린더 생산성 툴, `web.akiflow.com/#/planner/today`)

## 현재 상태 (최근 세션 2026-06-23 "세션 3 재기동" 기준)
- **dev 서버**: `localhost:5180` (strictPort) · **CDP 포트**: 9222, 프로필 `/tmp/akiflow-ref-chrome`
- **harness 패턴**: `peek.py`(실물, read-only attach) + `cap.py`(클론) 분리, 그 외 `parity.py`/`introspect.py`/`gen_flow.py`/`gate.py`/`flow.py`/`glyph_diff.py` 등
- **티켓**: M2 코어 10/10 PASS, M3-UI 4/4 PASS, Polish P1/P2 PASS. P3(Rituals recap 충실도)만 미완.
- **파리티 게이트**: `parity.py` 케이스 15→24로 성장, 최신 "parity 24/24 무결". 동작 커버리지 `_FLOW_MATRIX.md` 53개 흐름 중 31/53→52/53(R8 세션). 통합 게이트 `gate.py` 최신 출력: **"GATE PASS 3/3"**(parity 24/24 · flow 56/56 · glyph mismatch 0), tsc 0 errors.
- **⚠ 메모리 정정**: 기존 세컨드브레인 메모리는 "M1 빌드 대기"로 기록되어 있었으나 이는 **stale** — 실제로는 recon(M0)·M1 셸·M2(10티켓)·M3-UI(4티켓)·Polish P1/P2·갭배치 A/B/C/D(12/16 적용)까지 완료하고 현재 픽셀파리티/동작커버리지 정밀화 루프(`gate.py`)에 있음.

## 이 캠페인이 낳은/공유한 기법
- [[techniques.port-profile-isolation]] — 9222/5180 격리 조합의 원 사례(다른 두 캠페인의 포트 배정 기준점)
- [[techniques.regression-harness-suite]] — `gate.py`의 3축 통합 게이트가 이 패턴의 진화형 사례
- [[pipelines.night-run]] — cmux 기반 무인 오케스트레이터 킥오프(`_ORCH_KICKOFF.md`)가 vault SSOT(야간-무인-복제-시스템)를 그대로 채택

## 현재 캠페인 루프

정찰 완료(M0) 후 **일시정지** 상태 — 재개 시 clone-kb 무기고(스킬 로딩 패턴)로 최신 기법 세트를 장착하고 M1 빌드부터.

## 잔여 티켓 / 남은 일
- P3 Rituals recap 충실도 — 유일한 미완 티켓.
- B1(다크테마 필 색상 — 실물이 라이트 모드에 고정돼있어 측정 불가, 강제전환은 안전경계 위반이라 보류), B2(미래 날짜 메타-필 표시 — 실물이 해당 상태를 현재 노출 안 함).
- B7(실물 앱이 Daily Ritual 인트로 화면에 멈춰 메인뷰 측정 차단) — 일시적/보류 상태로 재확인됨.
- M3 실연동(Google Calendar/Todoist/Aki AI OAuth·백엔드)은 사용자 결정으로 명시적 보류.

## 최근 세션
2026-06-23 (R8 스윕 완료, GATE PASS 3/3).
