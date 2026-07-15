---
id: techniques.cdp-raw-driver
title: CDP Raw 드라이버 (좀비 탭 우회)
doctype: technique
status: verified
proven_in: [canvas]
related: [techniques.cdp-nondestructive-recon, techniques.rip-css-dump]
evidence:
  - "260615_canvas-clone/harness/cdp_raw.py — CdpSession(url_substr, cdp_http) 단일 healthy 타겟에만 raw websocket attach, Page.bringToFront 매 init마다 호출"
  - "2026-07-13 REC-G 세션 도입 — '이 세션 최대 시간 소모 버그'로 기록"
  - "260615_canvas-clone 커밋 7b0e950(2026-07-16, 세션17) — CdpSession 다중탭 매칭 모호성 → 시끄럽게 실패하도록 가드 신설. 계기: 동일 dev포트(5175) 2탭에서 substring이 비결정적으로 엉뚱한 탭에 attach해 클론 자율생성 프로젝트 doc.json이 오토세이브로 2회 빈 채 덮어써짐(백업 복원, 데이터 유실 0)"
updated: 2026-07-16
owner: 박춘순
---

# CDP Raw 드라이버 (좀비 탭 우회)

**한 줄**: Playwright의 `connect_over_cdp()`는 브라우저의 **모든** 타겟에 attach를 시도하다 죽은("좀비") 탭 하나 때문에 180초씩 행업된다. 이를 피해 raw 웹소켓으로 원하는 타겟 하나에만 직접 붙는다.

## 문제 상황 (실제 발견 경위)
canvas-clone 세션에서 특정 탭(`766028e1-...`)이 `Runtime.enable`/`Page.enable`에 6초 이상 무응답 — JS 다이얼로그가 뜬 것도 아닌 "진짜 좀비 렌더러" 상태. Playwright는 전체 타겟을 순회하며 attach하므로 이 탭 하나 때문에 스크립트 전체가 멈춤.

## 어떻게 (harness/cdp_raw.py)
- `CdpSession(url_substr, cdp_http="http://localhost:9222")`: URL 부분 문자열로 매칭되는 **건강한 타겟 하나만** raw websocket으로 attach.
- Page/DOM/Runtime 도메인만 활성화.
- `Page.setInterceptFileChooserDialog` 설정.
- **매 init마다 `Page.bringToFront` 호출** — 백그라운드 탭(`document.hidden=true`)은 rAF/CSS transition이 스로틀링되어, 클릭·키 이벤트는 정상 발생하는데 줌 같은 애니메이션 의존 상태가 조용히 갱신 안 되는 문제가 있었음. 이게 "이 세션 최대 시간 소모 버그"로 기록될 만큼 디버깅이 오래 걸림.

## 왜 중요한가
- 좀비 탭은 흔한 상황이 아니라 예외적으로 보이지만, 한 번 걸리면 스크립트가 전부 멈춰서 무인 야간 런 전체가 마비된다.
- `bringToFront`는 [[techniques.night-run-sop]]의 "포커스 스틸 금지" 규칙과 충돌하는 것처럼 보이지만, 여기서는 **자기 소유의 클론 탭**에 대해서만 쓰는 것이고 사람 작업 중인 다른 탭을 건드리지 않는다는 전제 — 다른 캠페인에 이식할 때 이 경계를 명확히 할 것.

## 함정
- `bringToFront`를 남용하면 사람이 다른 작업 중일 때 포커스를 뺏을 수 있다 — 반드시 자기 소유 클론/샌드박스 탭에만 한정.
- **멀티탭 substring 비결정성 (2026-07-16 세션17, 실제 데이터 손상 유발)**: `url_substr` 매칭이 "부분 문자열 포함하는 첫 healthy 타겟"을 잡는 방식이라, 같은 dev 포트(예: `localhost:5175`)에 탭이 2개 이상 열려 있으면 **어느 탭에 붙을지 비결정적**이다. canvas-clone에서 이 때문에 빌더 세션이 오래된/다른 프로젝트 탭에 attach해 클론 자율생성 프로젝트(`canvas-projects/cb30b89ae3d4/doc.json`)를 빈 상태로 2번 오토세이브해 덮어씀 — 백업에서 즉시 복원해 데이터 유실은 없었으나, 발견이 늦었으면 산출물이 조용히 사라질 뻔했다. **근본수정**: 다중 매칭 시 조용히 첫 번째를 고르지 않고 **즉시 시끄럽게 실패**(에러 raise, 후보 목록 출력)하도록 `CdpSession` 초기화 로직에 가드 추가. **운용 규칙**: 무인 런에서는 탭당 1빌더·canvas-id를 고정해 애초에 모호성이 생길 상황을 피한다.

## 관련
- [[techniques.cdp-nondestructive-recon]] — 이 드라이버가 뒷받침하는 상위 정찰 원칙
