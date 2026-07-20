---
id: techniques.non-intrusive-browser-automation
title: 비침습 브라우저 자동화 — 오너 기기를 공유하며 포커스를 뺏지 않기
doctype: technique
status: verified
proven_in: [notion]
related: [techniques.dom-first-measurement, techniques.pixel-diff-baseline, techniques.regression-harness-suite]
updated: 2026-07-20
owner: 박춘순
---

# 비침습 브라우저 자동화 (Non-Intrusive Browser Automation)

**한 줄**: 클론 캠페인은 오너와 **같은 기기·같은 화면**에서 돌아간다. 자동화가 창을 전면으로 끌어오면 **오너 키입력이 꼬여 작업이 중단**된다. 목적별로 브라우저를 나눠 쓰고, 포커스를 건드리는 호출을 전면 금지한다.

## 왜 (notion 캠페인 실증)

무인/반자동 런 중 오너가 반복 호소: *"자꾸 네가 포커스 가져가서 내 키입력이랑 꼬여"*, *"새 탭 만들 때마다 포커스 가져가"*. 원인은 워커들이 습관적으로 쓰던 세 가지 — `page.bring_to_front()`, osascript `activate`, 그리고 **`context.new_page()`(새 탭이 전면으로 뜸)**. 자동화 자체는 백그라운드로 충분히 가능한데 불필요하게 화면을 점유하고 있었다.

## 규칙

### 1. 포커스를 뺏는 호출 금지
- ❌ `page.bring_to_front()` · `window.focus()` · osascript `tell application ... activate`
- ❌ `context.new_page()` / `browser.new_page()` — **새 탭도 전면으로 뜬다**
- ✅ 기존 탭 재사용: `context.pages`에서 URL로 골라 `Page.navigate`/`Runtime.evaluate`
- ✅ 새 탭이 정말 필요하면 **CDP `Target.createTarget`에 `background: true`** (뒤에서 조용히 열림), 끝나면 `Target.closeTarget`

### 2. 백그라운드 CDP로 충분하다
| 목적 | 호출 | 포커스 |
|---|---|---|
| DOM·computed CSS 계측 | `Runtime.evaluate` | 불필요 |
| 키 입력 재현 | `Input.dispatchKeyEvent` | 불필요(백그라운드 탭에도 전달) |
| 클릭·드래그 | `Input.dispatchMouseEvent` | 불필요 |
| 스크린샷 | `Page.captureScreenshot` | 불필요 |
| **trusted OS 입력**(IME 한글 조합·클립보드 커스텀 MIME) | osascript | **필요 — 사전 승인** |

마지막 줄만 예외다. 그 경우 **작업 전 오너에게 알리고 최소 시간만 점유 후 반환**한다.

### 3. ★역할 분리 — 계측은 headless, 픽셀은 headful
포커스 문제를 구조적으로 없애되 **측정 신뢰도를 깨지 않는** 분리:

- **headless = 워커 작업의 대부분** (DOM·CSS 계측, 동작 재현, 게이트 실행, 버그 재현). 렌더 엔진이 같아 이 영역은 headful과 결과가 동일하고, 탭을 몇 개 만들든 화면에 안 뜬다.
- **headful = 픽셀 비교 캡처 전용**. 픽셀 파리티는 **원본(headful)과 동일 렌더 조건**이어야 유효한데, headless는 폰트 서브픽셀 렌더가 미묘하게 달라 **클론만 headless로 찍으면 수치가 오염**된다. [[techniques.pixel-diff-baseline]]의 "동일조건 캡처" 원칙이 무너지므로 픽셀만은 기존 headful 창에서, 그것도 기존 탭 재사용으로.
- 원본 앱(로그인 세션이 있는 창)은 세션 유지 때문에 현행 창 + 기존 탭 1개 재사용.

### 4. 구현 노트 (실측)
- ✅ `p.chromium.launch(headless=True)` + `new_page(viewport=...)` — 정상 동작 검증(2026-07-20, 클론 dev 서버 구동·DOM 판독).
- ⚠ 상시 `--headless=new --remote-debugging-port=<port>` 인스턴스는 macOS/Chrome-for-Testing 조합에서 **포트 바인딩 실패**를 겪음(프로세스는 뜨나 CDP 미개방, 로그도 비어 있음). → **상시 인스턴스에 의존하지 말고 워커가 필요할 때 launch → 작업 → `finally: close`**.
- 워커가 만든 여분 탭은 작업 종료 시 정리(누적되면 다음 세션의 탭 선택 로직이 오염된다 — 실제로 잔재 탭 15개가 쌓인 사례).

## 적용 체크리스트

- [ ] 브리프/정책에 "포커스 탈취 금지" 명문화 (워커는 새 컨텍스트라 매번 읽어야 함)
- [ ] 계측·동작·게이트 → headless 경로
- [ ] 픽셀 캡처 → headful 기존 탭
- [ ] 새 탭 필요 시 `Target.createTarget(background:true)` + 종료 시 정리
- [ ] osascript가 필요한 시나리오는 별도 표시 + 사전 승인

## 실증

- **notion(2026-07-20)**: 오너 3회 호소 → 정책 §브라우저에 금지 규칙 + 역할 분리 확립, 가동 중 워커 2명에 즉시 주입. 이후 계측·게이트·재현은 전부 백그라운드로 수행 가능함을 확인.
