---
id: techniques.url-escape-guard
title: URL 이탈 가드 (크롤러 실수 네비게이션 방어)
doctype: technique
status: verified
proven_in: [canvas]
related: [techniques.rip-crawler, techniques.cdp-nondestructive-recon]
evidence:
  - "260615_canvas-clone/ref/_RIP_CRAWL_PILOT.md — 로고 클릭이 higgsfield.ai/asset/all로 실제 네비게이션된 실물 사고, 이를 크롤러가 포착 후 URL 가드 신설(second line of defense)"
  - "260615_canvas-clone/harness/rip_crawl.py — BLOCK_TEXT_SUBSTRINGS + URL 변화 감시"
updated: 2026-07-13
owner: 박춘순
---

# URL 이탈 가드 (크롤러 실수 네비게이션 방어)

**한 줄**: 자동 크롤러가 실물 앱을 헤집다 보면 로고/링크 클릭 같은 걸로 **의도치 않게 앱 밖으로 네비게이션**될 수 있다. 액션 실행 후 현재 URL이 예상 범위를 벗어났는지 감시해서 즉시 잡아낸다.

## 발견 경위 (실제 사고)
canvas-clone의 [[techniques.rip-crawler]] 파일럿 실행 중, 실물 캔버스의 로고를 클릭하는 후보가 실행되며 실제로 `higgsfield.ai/asset/all`로 네비게이션되어버린 사고가 발생. 이건 [[techniques.cdp-nondestructive-recon]]의 "실물은 read-only, 비파괴" 원칙을 정면으로 깨는 상황 — 이 사고 자체가 크롤러의 **실전 유용성을 증명하는 사례**가 됐다(사람이 미리 못 막았던 걸 자동화가 잡아냄) 그리고 동시에 "두 번째 방어선"의 필요성을 확정지음.

## 어떻게
- 크롤러(`rip_crawl.py`)에 텍스트 기반 1차 방어(`BLOCK_TEXT_SUBSTRINGS` — GENERATE/Invite/Share/Delete/Undo/Duplicate/Log out 등)가 이미 있었지만, **로고 클릭처럼 텍스트 없는 아이콘성 컨트롤**은 이 방어를 통과했다.
- 이후 URL 변화 자체를 감시하는 가드를 추가 — 액션 실행 전후 URL을 비교해 도메인/경로가 baseline을 벗어나면 즉시 원상복구(뒤로가기/직접 URL 재설정) + 해당 후보를 크롤 대상에서 제외.

## 왜 "두 번째 방어선"인가
텍스트 블록리스트(1차 방어)는 "위험해 보이는 이름"에만 반응한다. 아이콘·로고처럼 텍스트가 없는 컨트롤은 애초에 걸러지지 않으므로, **결과(네비게이션 발생 여부)를 직접 감시**하는 게 유일하게 확실한 2차 방어다.

## 함정
- 1차 방어(텍스트 블록리스트)만 믿고 2차(결과 감시)를 생략하면 이런 사고가 재발한다 — 두 레이어를 항상 같이 둘 것.

## 관련
- [[techniques.rip-crawler]] — 이 가드가 보호하는 상위 크롤러
