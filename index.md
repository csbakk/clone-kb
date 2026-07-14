# index — 전체 색인 (한 줄, 질의는 여기부터)


## techniques/
- [적대적 검증 (빌더 ≠ 검증자, verify-first 루프)](techniques/adversarial-verification.md) — standard
- [애니메이션 리퍼 (트랜지션 지문 일치)](techniques/animation-ripper.md) — experimental
- [Append-only 로깅 (워크로그·티켓·갭매트릭스)](techniques/append-only-logging.md) — standard
- [원자적 localStorage 주입 (bulk_inject)](techniques/atomic-localstorage-inject.md) — verified
- [블라인드 A/B 판별 테스트 (사람 눈으로 최종 확인)](techniques/blind-ab-test.md) — experimental
- [CDP 비파괴 정찰 (peek 패턴, 리로드 금지)](techniques/cdp-nondestructive-recon.md) — standard
- [CDP Raw 드라이버 (좀비 탭 우회)](techniques/cdp-raw-driver.md) — verified
- [클립보드 JSON을 정본으로 (노드캔버스 앱)](techniques/clipboard-source-of-truth.md) — standard
- [크로스-페이스트 파리티 (라운드트립 diff 0)](techniques/cross-paste-parity.md) — verified
- [실사용(dogfooding)으로 버그 발견 — BORI 사례](techniques/dogfooding-as-bug-discovery.md) — verified
- [DOM 기반 측정 (픽셀 스샷 대체)](techniques/dom-first-measurement.md) — standard
- [모델 매트릭스 diff (카탈로그 전수 검증, GENERATE 비용 0)](techniques/model-matrix-diff.md) — verified
- [야간 무인 런 SOP (graceful skip · 안전경계 · 큐)](techniques/night-run-sop.md) — standard
- [오케스트레이터 모델 라우팅 (fable 오케 / sonnet 빌더 / opus 검증)](techniques/orchestrator-model-routing.md) — standard
- [osascript 트러스티드 입력 하이브리드 (한글 IME 우회)](techniques/osascript-trusted-hybrid.md) — verified
- [파리티 CI (교차앱 자동 회귀 파이프라인)](techniques/parity-ci.md) — experimental
- [파리티 감시 데몬 (99% 선언 이후 유지)](techniques/parity-watch-daemon.md) — experimental
- [픽셀 지문 게이트 (≥99% 점수 재현성)](techniques/pixel-fingerprint-gate.md) — experimental
- [픽셀 스크린샷을 1차 오라클로 (은퇴)](techniques/pixel-screenshot-as-primary-oracle.md) — retired
- [포트+프로필 격리 (프로젝트당 전용 CDP 포트·Chrome 프로필)](techniques/port-profile-isolation.md) — standard
- [호버 중 레코딩 (Clone Inspector + ci_agent)](techniques/record-during-hover.md) — verified
- [번호매김 회귀 검증 스위트 (_bN_verify.py / *_gate.py)](techniques/regression-harness-suite.md) — standard
- [RIP 레이어② 인터랙션 크롤러](techniques/rip-crawler.md) — verified
- [RIP 레이어① CSS/DOM 전수 덤프](techniques/rip-css-dump.md) — standard
- [RIP 레이어③ 자동 수복 루프](techniques/rip-repair-loop.md) — verified
- [상태 탐색기 (커버리지 % 자동 측정)](techniques/state-explorer.md) — verified
- [상태 명세 JSON (URL + 도달 절차 재현)](techniques/state-spec-json.md) — verified
- [서브에이전트 병렬화 규칙 (독립·무충돌만 병렬)](techniques/subagent-fanout-rules.md) — standard
- [트윈 미러 하네스 (실물·클론 동시 재생 비교)](techniques/twin-mirror-harness.md) — experimental
- [URL 이탈 가드 (크롤러 실수 네비게이션 방어)](techniques/url-escape-guard.md) — verified
- [자산 출처 게이트 (시각 자산 provenance — 자작 대체 재발방지)](techniques/asset-provenance-gate.md) — experimental
- [G1 비주얼 판정 시트 (bbox 오버레이 + 크롭)](techniques/visual-triage-sheet.md) — verified

## pipelines/
- [99% 파리티 판정식 (v2 — 6축 게이트)](pipelines/99-percent.md) — verified
- [야간 무인 런 파이프라인](pipelines/night-run.md) — standard
- [RIP 파이프라인 v1 (전수 리핑 3단 조립도)](pipelines/rip-v1.md) — standard
- [Verify-First 루프 (측정→대조→티켓→구현→검증→커밋)](pipelines/verify-first-loop.md) — standard

## runs/
- [2026-07-14 canvas 세션12 — 오너 트리아지 판정 소비 (오케=opus)](runs/2026-07-14-canvas-s12-triage-consume.md) — done: -880(누적 -9.2%)
- [2026-07-14 canvas 세션11 — P2 델타 소탕+탐사기 승격 (무인 10h)](runs/2026-07-14-canvas-p2-deltasweep-explorer.md) — done: 델타 -14.6%·탐사기 파일럿 성공(게이트 §AA)
- [2026-07-13 canvas 세션10 — P1 크로스-페이스트 파일럿](runs/2026-07-13-canvas-p1-crosspaste.md) — done: P1 게이트 통과(왕복 diff 0)

## cases/
- [캠페인 사례 — Akiflow 클론 (260622_akiflow-clone)](cases/akiflow.md) — verified
- [캠페인 사례 — Higgsfield Canvas 클론 (260615_canvas-clone)](cases/canvas.md) — verified
- [캠페인 사례 — Notion 클론 (260622_notion-clone)](cases/notion.md) — verified
