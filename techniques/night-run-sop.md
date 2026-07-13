---
id: techniques.night-run-sop
title: 야간 무인 런 SOP (graceful skip · 안전경계 · 큐)
doctype: technique
status: standard
proven_in: [kit, notion, akiflow, canvas]
related: [techniques.port-profile-isolation, techniques.append-only-logging, techniques.subagent-fanout-rules, techniques.adversarial-verification, pipelines.night-run]
evidence:
  - "clone-campaign-kit/NIGHT-RUN.md — 큐 pull→measure→build→self-verify→gap0까지 자가수정→gate→commit / 막힘→_BLOCKED.md 기록→skip"
  - "clone-campaign-kit/knowledge/야간-무인-복제-시스템.md §6 — 안전경계(write scope=clone/만, 실물=read-only, per-task git commit 롤백, 금지행위 목록)"
  - "260622_notion-clone/ref/_AUTONOMOUS_10H_0712_RUN2.md, _AUTONOMOUS_10H_0713_RUN3.md — 실제 10시간 무인 런 2회 수행, RIP 델타 30%↓ 등 실적"
  - "260622_akiflow-clone/_ORCH_KICKOFF.md — cmux 기반 무인 오케스트레이터 킥오프, 야간-무인-복제-시스템.md를 SSOT로 인용"
updated: 2026-07-13
owner: 박춘순
---

# 야간 무인 런 SOP (graceful skip · 안전경계 · 큐)

**한 줄**: 사람 없이 밤새 도는 루프는 "막히면 멈추지 않고 우아하게 건너뛴다"가 핵심 규율이다. 절대 멈추지도, 무한루프에 빠지지도, 막힌 걸 억지로 뚫지도 않는다.

## 루프 형태
```
큐(_TICKETS.md) pull
  → measure(실물, 추측 0)
  → build
  → self-verify(parity.py → _GAPS.md)
  → gap 0까지 자가수정
  → gate 통과?
      → 통과: git commit → 다음 티켓
      → 막힘: _BLOCKED.md 기록 → skip → 다음 티켓
```

## 3계층 운영 (하루 사이클)
1. 사람 10~15분 (자기 전): 큐 우선순위 정리, 시작 트리거.
2. AI 무인 밤새: 위 루프 반복.
3. 사람 5분 (아침): `_BLOCKED.md` + 커밋 로그만 훑고 다음 지시.

## 안전경계 (반드시 지키는 것)
- **쓰기 범위**: `clone/` 디렉토리만. 실물 앱은 read-only(peek, 비파괴 — [[techniques.cdp-nondestructive-recon]]).
- **롤백**: 태스크 단위 git commit — 문제 생기면 그 커밋만 되돌리면 됨.
- **토큰/시간/비용 상한** 설정.
- **금지행위**: 무맹목 삭제, 실데이터 변경(mutation), CDP 브라우저 강제 종료, 파괴적 shell 명령.
- **완료 판단은 디스크 산출물로만** — 워커의 자가보고를 신뢰하지 않는다(→ [[techniques.adversarial-verification]]와 동일 뿌리). `pgrep -f <script>.py`로 생존 확인(`.py` 없이 grep하면 오탐).
- **막힘 카운트 기본 5회 초과 시** 부분 결과 저장하고 정지 — 무한 재시도 금지.
- Chrome은 CDP 포트당 동시 1워커로 직렬화(→ [[techniques.port-profile-isolation]]). git/localStorage 쓰기도 직렬화.
- `bringToFront` 같은 포커스 스틸 호출은 워크어라운드 로직에서도 절대 금지(백그라운드 탭 CPU 스로틀링 문제와 별개로 사람 작업을 방해).
- 좀비 `about:blank` 탭 복구 레시피: 탭 닫기 → 15초 쿨다운 → `/json/new?url=<target>` 직접 오픈.

## 실제 실적
- notion-clone: 10시간 무인 런 2회(RUN2, RUN3) 수행. RUN3에서 RIP 구조 델타 1539→1083(-30%), 캘린더 뷰는 157→18(-88.5%)까지 축소.
- akiflow-clone: cmux 오케스트레이터 킥오프 문서가 이 SOP(정본: 야간-무인-복제-시스템.md)를 그대로 인용해 시작.

## 함정
- "산출물 0·규칙위반 사고"가 실제로 있었음(2026-07-11/12) — 워커가 백그라운드 알림을 기다리며 결과를 저장하지 않고 끝난 사고. 이후 "백그라운드 알림 대기 없이 결과 즉시 저장" 규칙이 워커 프롬프트에 필수 문구로 추가됨.

## 관련
- [[pipelines.night-run]] — 이 SOP를 조립한 상위 파이프라인 문서
