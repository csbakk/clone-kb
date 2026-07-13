---
id: techniques.append-only-logging
title: Append-only 로깅 (워크로그·티켓·갭매트릭스)
doctype: technique
status: standard
proven_in: [canvas, notion, akiflow, kit]
related: [techniques.regression-harness-suite, techniques.night-run-sop, pipelines.night-run]
evidence:
  - "260622_notion-clone/_PROCESS.md §로깅규칙 — '불변 규칙: 모든 로그 줄에 T##+날짜. 로그는 수정 금지, append만.' _WORKLOG.md/_PARITY_LOG.md 헤더에 '(append-only)' 명시"
  - "260615_canvas-clone/ref/_VERIFY_r1.md — A→U 알파벳 섹션 append, 정정은 새 섹션(§E가 §A-D를 재검증)으로 추가, 덮어쓰기 없음"
  - "260615_canvas-clone/ref/_GAPS_r1_shell.md ~ _GAPS_r5_shellsurfaces.md — 영역별 번호매김 갭매트릭스, 회차마다 새 파일"
  - "clone-campaign-kit/knowledge/야간-무인-복제-시스템.md — Spec(현재 진실) ≠ Log(시간순) ≠ Decision(왜, ADR) 3계층 명시적 분리"
updated: 2026-07-13
owner: 박춘순
---

# Append-only 로깅 (워크로그·티켓·갭매트릭스)

**한 줄**: 워크로그·검증로그·갭매트릭스는 **절대 수정하지 않고 새 줄/새 섹션만 추가**한다. 정정이 필요하면 새 항목으로 덧붙인다.

## 3계층 문서 분리 (핵심 원칙)
| 계층 | 성격 | 예시 |
|---|---|---|
| Spec | 지금 시점의 진실 (덮어써도 됨) | CLONE-METHOD.md, RIP-PIPELINE.md |
| Log | 시간순 기록 (append-only, 절대 수정 금지) | _WORKLOG.md, _PARITY_LOG.md, _GAPS_r*.md |
| Decision | 왜 그렇게 했나 (ADR, 불변·추가만) | _DECISIONS.md |

## 왜 필요한가
- 무인 야간 런은 여러 세션이 이어달리기로 진행된다. 이전 세션이 뭘 했는지, 왜 그런 판단을 내렸는지가 **그 시점 기준으로 그대로 남아있어야** 다음 세션(사람이든 AI든)이 신뢰하고 이어갈 수 있다.
- 로그를 수정 가능하게 열어두면 "그때는 맞았는데 지금 틀렸다고 지워버리는" 식으로 판단 이력이 사라진다 — 근거 추적이 끊긴다.
- canvas `_VERIFY_r1.md`의 실제 패턴: §A~D에서 검증한 항목을 §E가 재검증하며 "§A-D 수정사항 재검증"이라고 명시 — 원본 §A-D는 그대로 두고 §E를 새로 추가. 최종 판정은 맨 뒤 §F.

## 어떻게
- 로그 파일 상단에 성격을 명시 (`# WORKLOG — 개발 로그 (append-only)`).
- 모든 줄에 타임스탬프/티켓 ID를 박아서 시간순 정렬이 항상 가능하게 (notion `_PROCESS.md`: "모든 로그 줄에 T##+날짜").
- 정정·재검증은 새 섹션(알파벳/번호 이어감)으로 — 기존 섹션은 손대지 않음.
- 갭매트릭스처럼 회차성 문서는 파일명에 회차 번호를 박아 새 파일로 분리 (`_GAPS_r1_shell.md` → `_GAPS_r5_shellsurfaces.md`).

## 함정
- append-only를 지키려다 파일이 무한정 커지는 문제 — canvas `_VERIFY_r1.md`는 109KB까지 성장. 회차별 파일 분리(갭매트릭스 방식)로 완화 가능.

## 관련
- [[techniques.night-run-sop]] — 이 로깅 규율이 없으면 무인 런의 완료판단(디스크 기준)이 성립하지 않음
