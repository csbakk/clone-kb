---
id: techniques.coordinate-click-capture
title: 좌표-클릭 캡처 (DOM 셀렉터 실패 시 CDP 좌표 마우스)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.webgl-node-rendering-clone, techniques.osascript-trusted-hybrid, techniques.cdp-nondestructive-recon, techniques.canvas-clipboard-localstorage]
evidence:
  - "260615_canvas-clone harness/real_archive.py:78 (2026-07-18) — `.react-flow__node` 셀렉터가 WebGL 이관 후 매치 0이 되면서, 캔버스 포커스·노드 선택을 `pg.mouse.click(350, 750)` 화면 좌표 클릭으로 대체(이후 Meta+A/Meta+C로 전체선택→복사). DOM 셀렉터 경로가 막힌 지점을 좌표 클릭이 대신 뚫은 실측 사례"
  - "260615_canvas-clone ref/real-recapture-2026-07-18/nodes/video/current/{V02_selected_full,V03_inspector}.png (2026-07-18) — 노드를 화면 좌표 클릭으로 선택(V02)한 직후 우측 인스펙터 패널이 DOM으로 열림(V03) — 노드 자체는 WebGL 픽셀이라 셀렉터 타겟이 없지만, CDP가 좌표를 캔버스에 hit-test해 앱의 클릭 핸들러를 정상 트리거하고 그 결과(인스펙터)는 다시 DOM이라 통상 캡처 가능함을 확인"
  - "260615_canvas-clone harness/osinput_lock.py + harness/_COORDINATION.md (2026-07-18) — CDP-to-own-browser 입력(Playwright `mouse.click`/`keyboard.press` via `connect_over_cdp`)은 해당 브라우저 페이지에만 가고 OS 커서/키보드를 안 건드려 세션 간 충돌이 없음(락 불요, 기본 방식)과 대조적으로, OS 전역 입력(osascript/cliclick/pyautogui)은 물리 입력이라 `osinput_lock.py`(`/tmp/hf_osinput.lock`, 60s 스테일 탈취)로 반드시 상호배제해야 함을 문서화"
updated: 2026-07-18
owner: 박춘순
---

# 좌표-클릭 캡처 (DOM 셀렉터 실패 시 CDP 좌표 마우스)

**한 줄**: 캔버스/WebGL로 렌더되는 요소([[techniques.webgl-node-rendering-clone]])는 DOM 셀렉터로 타겟팅할 수 없다 — 대신 **화면 좌표로 CDP 마우스 클릭**(`mouse.click(x, y)`)을 쏘면 브라우저가 그 좌표를 캔버스에 hit-test해 앱의 클릭 핸들러가 정상 동작한다. 셸/툴바/인스펙터/메뉴는 DOM 셀렉터, **캔버스 노드만** 좌표 클릭의 하이브리드.

## 언제 쓰나
- `.react-flow__node`류 DOM 셀렉터 매치가 0인데 화면엔 노드가 보일 때(= WebGL 렌더 확정, [[techniques.webgl-node-rendering-clone]] 3-신호 참고).
- 노드를 선택/클릭해야 우측 인스펙터가 열리는데, 노드 자체엔 셀렉터로 잡을 DOM이 없을 때.
- 캔버스 전체를 포커스시켜야 키보드 단축키(Cmd+A 전체선택 등)가 캔버스로 라우팅될 때.

## 어떻게 (하이브리드 3층)
1. **DOM 셀렉터** — 셸/툴바/인스펙터/메뉴/모달은 여전히 DOM이므로 통상 `page.click('[aria-label=...]')` 등 그대로 사용.
2. **좌표 마우스(CDP)** — 캔버스 위 노드는 `page.mouse.click(x, y)`로 화면 좌표를 직접 클릭. 실측(real_archive.py:78): 빈 캔버스 영역 좌표 클릭 → 포커스 확보 → 이후 `Meta+a`(전체선택)/`Meta+c`(복사) 키 이벤트가 캔버스로 정상 라우팅됨. 노드를 특정해 클릭할 때도 같은 방식 — 노드의 화면상 bounding box 중심 좌표를 스크린샷/줌 상태에서 계산해 클릭하면 앱이 그 좌표를 hit-test해 노드 선택 → 인스펙터(DOM)가 열린다.
3. **localStorage-clipboard(bulk 조작)** — 다수 노드 조작(전체 정렬·재배치 등)은 좌표 클릭 반복 대신 [[techniques.canvas-clipboard-localstorage]] + [[techniques.canvas-coord-inject-rearrange]]의 클립보드 JSON 경로가 더 안정적. 좌표 클릭은 "선택/열기" 같은 **단발 인터랙션**에, 클립보드 경로는 **구조 변경**(좌표 재계산 등)에 쓴다.

## 입력 격리 — CDP vs OS 전역 (충돌 여부가 다름)
- **CDP-to-own-browser 입력**(`connect_over_cdp` 후 `mouse.click`/`keyboard.press`)은 그 브라우저 페이지에만 가고 **OS 커서/키보드를 안 건드린다** — 다른 세션과 충돌 없음, 락 불필요. 좌표-클릭 캡처는 기본적으로 이 경로.
- **OS 레벨 입력**(osascript/System Events 등, [[techniques.osascript-trusted-hybrid]] 같은 trusted 입력이 필요할 때만)은 물리 입력이라 여러 세션이 동시에 쓰면 큐가 겹친다 — 반드시 공유 락(`harness/osinput_lock.py`, `/tmp/hf_osinput.lock`)으로 직렬화.
- 요약: 좌표 클릭이 CDP 경로로 충분하면 락 불필요. untrusted 이벤트로 앱이 반응 안 해(예: Cmd+V 키다운 무반응) osascript로 전환해야 하는 경우에만 락을 잡는다.

## 함정
- 좌표는 **줌/팬 상태에 종속** — 캔버스가 스크롤/줌되면 같은 논리적 노드도 화면 좌표가 바뀐다. 클릭 직전 항상 "Return to content"/fit-view로 상태를 고정하거나, 클릭 직전에 그 노드의 현재 bounding box를 재계산해야 한다.
- 좌표 클릭은 **어떤 노드를 클릭했는지 클릭 전에 검증할 방법이 없다**(DOM이 없으니 사전 assert 불가) — 클릭 후 열린 인스펙터의 타이틀/필드로 사후 검증하는 패턴을 기본으로 삼는다.
- 다중 세션이 같은 브라우저 CDP 포트를 공유하면 좌표 클릭도 서로 충돌한다 — [[techniques.port-profile-isolation]]로 세션마다 전용 포트/프로필을 먼저 확보할 것.

## 관련
- [[techniques.webgl-node-rendering-clone]] — 이 기법이 필요해지는 원인(노드에 DOM 타겟이 없음)
- [[techniques.osascript-trusted-hybrid]] — OS 레벨 trusted 입력이 필요할 때의 다음 단계 + 공유 락 규약
- [[techniques.cdp-nondestructive-recon]] — 좌표 클릭도 비파괴 정찰 원칙(peek, 리로드 금지) 하에서 운용
- [[techniques.canvas-clipboard-localstorage]] — bulk 노드 조작은 좌표 클릭보다 이 경로가 낫다
