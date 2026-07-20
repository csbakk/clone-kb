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
| 키 입력 재현 | `Input.dispatchKeyEvent` | **⚠ 공유 headful 브라우저의 비활성 탭에선 드롭됨**(2026-07-20 실측) → **단명 headless launch**로 |
| 클릭·드래그 | `Input.dispatchMouseEvent` | 불필요 |
| 스크린샷 | `Page.captureScreenshot` | 불필요 |
| **trusted OS 입력**(IME 한글 조합·클립보드 커스텀 MIME) | osascript | **필요 — 사전 승인** |

마지막 줄만 예외다. 그 경우 **작업 전 오너에게 알리고 최소 시간만 점유 후 반환**한다.

### 3. ★headless 기본 — 전 축 동등 (실측 확정)
포커스 문제의 **근본 해결**은 headless다. 그리고 **측정 신뢰도를 깎지 않는다**:

- **canvas 캠페인 A/B 실측(2026-07-20)**: 레이아웃/computed CSS **바이트 동일**, 폰트(한글 포함) 육안 동일, **video 재생 정상**, CSS 트랜지션 중간값까지 일치. → **측정·회귀·픽셀·영상증거 전부 headless로 찍어도 된다.**
- ⚠ **이전 통념 "headless는 폰트 서브픽셀이 달라 픽셀 비교가 오염된다"는 추측이었고 반증됐다**(notion 세션이 근거 없이 정책에 넣었다가 canvas 실측으로 정정). 추측을 정책에 넣지 마라 — 이 카드 자체가 그 사례다.
- **필수 런치 플래그(빠뜨리면 조용히 틀린 결과가 나온다)**:
  `--headless=new --user-data-dir=<임시> --force-device-scale-factor=2 --autoplay-policy=no-user-gesture-required`
- 원본 앱(로그인 세션 창)은 headed 유지 + **기존 탭 재사용**. **헤디드 백그라운드 탭 캡처도 스테일하지 않다**(실측) — 캡처가 이상하다고 포커스로 해결하지 말고 headless로 옮겨라.

### 4. 구현 노트 (실측)
- ✅ `p.chromium.launch(headless=True)` + `new_page(viewport=...)` — 정상 동작 검증(2026-07-20, 클론 dev 서버 구동·DOM 판독).
- ⚠ 상시 `--headless=new --remote-debugging-port=<port>` 인스턴스는 macOS/Chrome-for-Testing 조합에서 **포트 바인딩 실패**를 겪음(프로세스는 뜨나 CDP 미개방, 로그도 비어 있음). → **상시 인스턴스에 의존하지 말고 워커가 필요할 때 launch → 작업 → `finally: close`**.
- ⚠**`--force-device-scale-factor=2`는 반드시 런치 플래그.** 런타임 CDP 오버라이드만 하면 `devicePixelRatio`는 2로 **맞게 보이는데 스크린샷/영상만 조용히 half-res**로 저장된다. 값만 보면 정상이라 가장 잘 속는 함정. **실사고**: notion 세션이 플래그 없이 headless로 찍은 증명 영상이 **550×420**으로 저장(같은 런의 headful 영상은 1200×900·1360×1000) — 판독 불가 수준.
- **대책 = 표준 런치 헬퍼**: 플래그를 고정한 단일 진입점을 만들고 손으로 `launch()` 하지 못하게 한다. 헬퍼 안에서 **`devicePixelRatio`와 실제 스크린샷 픽셀 폭을 둘 다 확인해 half-res면 시끄럽게 실패**시킬 것(조용한 재발 차단).
- 기타 함정: **오너 프로필 재사용 금지**(락 충돌) / 앱 루트 `/`는 대시보드 오버레이가 덮으므로 **앱 라우트로 이동 후 캡처** / `:hover` 재현은 `dispatchEvent`가 아니라 **CDP `page.mouse.move()`** / 두 브라우저 비교 전 **뷰포트 transform 안정까지 폴링**(안 하면 가짜 갭이 잡힌다).
- 워커가 만든 여분 탭은 작업 종료 시 정리(누적되면 다음 세션의 탭 선택 로직이 오염된다 — 실제로 잔재 탭 15개가 쌓인 사례).

## 적용 체크리스트

- [ ] 브리프/정책에 "포커스 탈취 금지" 명문화 (워커는 새 컨텍스트라 매번 읽어야 함)
- [ ] 클론 작업 전체 → **headless 기본**(표준 런치 헬퍼 경유, 손 launch 금지)
- [ ] 헬퍼가 dpr/스크린샷 실폭 자기검증하는지 확인(half-res 조용한 실패 차단)
- [ ] 새 탭 필요 시 `Target.createTarget(background:true)` + 종료 시 정리
- [ ] osascript가 필요한 시나리오는 별도 표시 + 사전 승인

## 크로스캠페인 정본

이 규칙은 clone-kb `PROTOCOL.md` §2.5(크로스캠페인 운영 결정, append-only)에도 등재돼 **모든 클론 세션에 즉시 적용**된다. 캠페인 리포의 `_POLICY.md`는 이 카드를 프로젝트값(포트·경로)으로 구체화한 사본이다([[pipelines.02-campaign-policy-standard]]).

## 실증

- **★실측 정정(2026-07-20, notion W-FH)**: "백그라운드 탭에도 키가 전달된다"는 통념은 **틀렸다** — 공유 headful 브라우저에서 비활성 탭의 `Input.dispatchKeyEvent`는 드롭된다. 마우스·계측·캡처는 백그라운드에서 정상이지만 **키 입력이 필요한 재현/영상은 단명 headless launch가 유일하게 안전한 경로**다(포커스도 안 뺏고 키도 먹는다).
- **notion(2026-07-20)**: 오너 3회 호소 → 정책 §브라우저에 금지 규칙 + 역할 분리 확립, 가동 중 워커 2명에 즉시 주입. 이후 계측·게이트·재현은 전부 백그라운드로 수행 가능함을 확인.
