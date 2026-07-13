---
id: techniques.port-profile-isolation
title: 포트+프로필 격리 (프로젝트당 전용 CDP 포트·Chrome 프로필)
doctype: technique
status: standard
proven_in: [canvas, notion, akiflow, kit]
related: [techniques.night-run-sop, techniques.cdp-nondestructive-recon, techniques.subagent-fanout-rules]
evidence:
  - "clone-campaign-kit/README.md §9 — akiflow 9222/5180, canvas 9223/5175, notion 9224/5185, next 9225/5190 테이블"
  - "260622_notion-clone/CLONE-METHOD.md·CLAUDE.md — 동일 테이블, 전용 프로필 ~/.chrome-notion-clone"
  - "__obsidian/wiki/concepts/웹앱-클론-캠페인-운영.md §6 — 동일 격리 테이블 (정본 소스)"
updated: 2026-07-13
owner: 박춘순
---

# 포트+프로필 격리 (프로젝트당 전용 CDP 포트·Chrome 프로필)

**한 줄**: 클론 프로젝트마다 CDP 디버그 포트 + dev 서버 포트 + Chrome user-data-dir을 전부 따로 쓴다. 포트만 다르고 프로필을 공유하면 세션이 섞인다.

## 확정 테이블 (3캠페인 + kit 표준)
| 프로젝트 | CDP 포트 | dev 포트 | Chrome 프로필 |
|---|---|---|---|
| akiflow | 9222 | 5180 | 전용 프로필 |
| canvas | 9223 | 5175 | ~/.chrome-canvas-clone |
| notion | 9224 | 5185 | ~/.chrome-notion-clone |
| (다음 프로젝트) | 9225 | 5190 | ~/.chrome-\<app\>-clone |

## 왜 필요한가
- **프로필 공유의 실제 사고**: 포트만 분리하고 프로필(user-data-dir)을 같이 쓰면 로그인 세션·localStorage·쿠키가 프로젝트 간에 섞인다. notion CLONE-METHOD.md에 명시적 경고: "포트만 다르고 프로필을 공유하면 세션이 섞이므로 user-data-dir도 반드시 분리."
- 여러 프로젝트를 동시에(또는 번갈아) 작업할 때 CDP attach가 엉뚱한 앱에 붙는 사고를 원천 차단.
- Chrome은 CDP 포트당 동시 1워커 직렬화가 원칙([[techniques.night-run-sop]]) — 포트가 프로젝트 정체성 그 자체가 된다.

## 어떻게
```
chrome --remote-debugging-port=<프로젝트포트> --user-data-dir=~/.chrome-<app>-clone
```
launch 스크립트(예: notion의 `harness/launch_chrome.sh`)로 고정해서 매번 같은 명령을 재현.

## 함정
- "다른 PC에서 클론 하나만 돌리면 충돌 없으니 기본값(9222/5173)도 무방" — 하지만 **프로필 분리는 그 경우에도 항상 유지**한다 (kit README §9).
- 안전장치 예: notion `bulk_inject.py`는 `CLONE_TAB_RE = r"^https?://localhost:5185(?:/|\?|#|$)"` 정규식으로 대상 탭 포트를 코드 레벨에서 다시 확인 — 사람 실수(다른 포트 탭에 잘못 씀)를 스크립트가 한 번 더 막음.

## 관련
- [[techniques.night-run-sop]] — 이 격리를 전제로 한 무인 런 안전경계
