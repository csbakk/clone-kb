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

### 2. 백그라운드 CDP로 충분하다 (단, 키 입력엔 함정이 있다)
| 목적 | 호출 | 포커스 |
|---|---|---|
| DOM·computed CSS 계측 | `Runtime.evaluate` | 불필요 |
| 키 입력 재현 | `Input.dispatchKeyEvent` | **⚠ 공유 headful 브라우저의 비활성 탭에선 드롭됨**(2026-07-20 실측) → 대상이 클론(로그인 불필요)이면 **단명 headless launch**(§3), 대상이 실물 로그인 세션 창이면 **포커스 에뮬레이션**(★§3.5, 아래) |
| 클릭·드래그 | `Input.dispatchMouseEvent` | 불필요(단 §3.6 buttons 플래그 함정 주의) |
| 스크린샷 | `Page.captureScreenshot` | 불필요 |
| **trusted OS 입력**(IME 한글 조합·클립보드 커스텀 MIME) | osascript | **필요 — 사전 승인** |

마지막 줄만 예외다. 그 경우 **작업 전 오너에게 알리고 최소 시간만 점유 후 반환**한다.

### 3. ★headless 기본 — 전 축 동등 (실측 확정, 클론 창 전용)
포커스 문제의 **근본 해결**은 headless다. 그리고 **측정 신뢰도를 깎지 않는다**:

- **canvas 캠페인 A/B 실측(2026-07-20)**: 레이아웃/computed CSS **바이트 동일**, 폰트(한글 포함) 육안 동일, **video 재생 정상**, CSS 트랜지션 중간값까지 일치. → **측정·회귀·픽셀·영상증거 전부 headless로 찍어도 된다.**
- ⚠ **이전 통념 "headless는 폰트 서브픽셀이 달라 픽셀 비교가 오염된다"는 추측이었고 반증됐다**(notion 세션이 근거 없이 정책에 넣었다가 canvas 실측으로 정정). 추측을 정책에 넣지 마라 — 이 카드 자체가 그 사례다.
- **필수 런치 플래그(빠뜨리면 조용히 틀린 결과가 나온다)**:
  `--headless=new --user-data-dir=<임시> --force-device-scale-factor=2 --autoplay-policy=no-user-gesture-required`
- 원본 앱(로그인 세션 창)은 headed 유지 + **기존 탭 재사용**. **헤디드 백그라운드 탭 캡처도 스테일하지 않다**(실측) — 캡처가 이상하다고 포커스로 해결하지 말고 headless로 옮겨라.
- ⚠ **headless는 "세션이 필요 없는 대상"에만 통한다** — 새 headless 인스턴스는 실물 앱의 로그인 쿠키를 안 갖고 있어 로그인 화면만 뜬다. 실물 로그인 세션 창(오너가 로그인해 둔 그 탭)엔 이 해법을 못 쓴다. 그 경우엔 아래 §3.5.

### 3.5 ★포커스 에뮬레이션 — 실물 로그인 세션 창에서 키 입력 (2026-07-20 확정, 최대 성과)

**"포커스 탈취 금지"와 "실물 로그인 세션 창에서 키 입력 자동화가 필요하다"는 겉보기엔 양립 불가능해 보였다.** §1 원칙대로 기존 탭을 재사용하면 그 창은 항상 OS 배경(비활성 탭)에 머문다. 그런데 크롬 렌더러는 비활성 탭을 `document.hidden===true`·`document.hasFocus()===false`로 취급해 **contenteditable 캐럿 배치·클립보드 이벤트·`Input.dispatchKeyEvent`가 막힌다**(§2 표의 근거). headless launch(§3)는 이 문제의 근본 해법이지만 **로그인 세션이 없는 새 인스턴스라 실물 창엔 적용 불가**하다 — 그래서 그동안 실물 창의 키 입력 재현은 사실상 막혀 있었다.

**해법**: CDP `Emulation.setFocusEmulationEnabled {enabled:true}` + `Page.setWebLifecycleState {state:'active'}`. 렌더러에게 "너는 지금 포커스·visible 상태"라고 스푸핑하는 CDP 표준 기능이다 — `document.hidden`→`false`, `document.hasFocus()`→`true`로 바뀌지만 **OS 레벨 포커스는 오너 손에 그대로 남는다**(창이 전면으로 뜨지 않음, 오너 키보드와 전혀 안 꼬임). 타깃(탭) 단위로 켜고, **작업이 끝나면 반드시 `enabled:false`로 원복**한다.

```
Emulation.setFocusEmulationEnabled {enabled: true}
Page.setWebLifecycleState {state: 'active'}
… 키 입력 · 클립보드 · 캐럿 조작 …
Emulation.setFocusEmulationEnabled {enabled: false}   # 작업 후 원복 필수(타깃 단위)
```

**비용 실증(이걸 몰랐던 대가)**: 이 해법을 찾기 전까지 같은 캠페인에서 fn-delete 실측 3회 연속 실패 + 마퀴(드래그 다중선택) 실측 실패 + 토글 여백 버그 재현 시도 2회 실패가 났다. 워커들은 "배경 탭이라 안 된다"고 정직하게 보류하거나, 엉뚱한 원인(스테일 서버 등)을 지목했다. **해소 직후 동일 부류 측정이 24/24 전량 성공**했고(fn-delete 24개 시나리오), 같은 인프라를 그대로 재사용해 대칭 설계된 Backspace 17개 시나리오까지 전수 측정(17/17)했다.

**기존 규칙과 모순 아님 — 대상이 다르다**:
| 대상 | 로그인 세션 | 해법 |
|---|---|---|
| 클론 창 | 불필요 | §3 headless 기본(새 인스턴스 자유롭게 launch) |
| 실물 창(오너 로그인 세션이 있는 그 창) | 필요 | **포커스 에뮬레이션**(기존 탭 재사용, 새 인스턴스 불가) |

headless가 "틀렸던" 게 아니다 — headless는 세션이 필요 없는 대상 전용이고, 포커스 에뮬레이션은 세션이 반드시 있어야 하는 실물 창을 커버하는 **짝 기법**이다. 둘 다 각자의 대상에서 여전히 유효하다.

### 3.6 구현 노트 (실측)
- ✅ `p.chromium.launch(headless=True)` + `new_page(viewport=...)` — 정상 동작 검증(2026-07-20, 클론 dev 서버 구동·DOM 판독).
- ⚠ 상시 `--headless=new --remote-debugging-port=<port>` 인스턴스는 macOS/Chrome-for-Testing 조합에서 **포트 바인딩 실패**를 겪음(프로세스는 뜨나 CDP 미개방, 로그도 비어 있음). → **상시 인스턴스에 의존하지 말고 워커가 필요할 때 launch → 작업 → `finally: close`**.
- ⚠**`--force-device-scale-factor=2`는 반드시 런치 플래그.** 런타임 CDP 오버라이드만 하면 `devicePixelRatio`는 2로 **맞게 보이는데 스크린샷/영상만 조용히 half-res**로 저장된다. 값만 보면 정상이라 가장 잘 속는 함정. **실사고**: notion 세션이 플래그 없이 headless로 찍은 증명 영상이 **550×420**으로 저장(같은 런의 headful 영상은 1200×900·1360×1000) — 판독 불가 수준.
- **대책 = 표준 런치 헬퍼**: 플래그를 고정한 단일 진입점을 만들고 손으로 `launch()` 하지 못하게 한다. 헬퍼 안에서 **`devicePixelRatio`와 실제 스크린샷 픽셀 폭을 둘 다 확인해 half-res면 시끄럽게 실패**시킬 것(조용한 재발 차단).
- ⚠ **`Input.dispatchMouseEvent`의 `mousemove`엔 `buttons:1`이 반드시 필요**(2026-07-20 실측) — 드래그 시퀀스에서 `mousePressed`(`buttons:1`) 이후 `mouseMoved`에 `buttons` 필드를 빼먹으면 브라우저가 "버튼 안 눌린 이동"으로 처리해 **마퀴·드래그가 시작조차 안 된다**. 조용히 무반응이라 "동작이 없다"는 잘못된 결론으로 이어지기 쉬움 — 드래그류 재현 스크립트는 매 mousemove에 `buttons`를 명시할 것.
- 기타 함정: **오너 프로필 재사용 금지**(락 충돌) / 앱 루트 `/`는 대시보드 오버레이가 덮으므로 **앱 라우트로 이동 후 캡처** / `:hover` 재현은 `dispatchEvent`가 아니라 **CDP `page.mouse.move()`** / 두 브라우저 비교 전 **뷰포트 transform 안정까지 폴링**(안 하면 가짜 갭이 잡힌다).
- 워커가 만든 여분 탭은 작업 종료 시 정리(누적되면 다음 세션의 탭 선택 로직이 오염된다 — 실제로 잔재 탭 15개가 쌓인 사례).

### 4. ★전용 CDP 드라이버 — 인라인 `python -c`는 세션 안전 분류기가 막는다 (2026-07-20)
실물 실측을 `python3 -c "<긴 인라인 스크립트>"` 형태로 돌리면, 이 형태는 사실상 "임의 코드 실행"이라 **세션 안전 분류기가 휴리스틱하게 차단**한다. 같은 명령이 통과했다 막혔다 하는 비결정적 거동이라, 워커가 이를 "배경 탭이라 안 된다" 같은 **환경 제약으로 오진**하는 부작용까지 낳는다(2026-07-20 하루에만 4회: fn-delete 관련 3회 + 마퀴 1회).

**해법**: CDP 원시 동작만 노출하는 **전용 서브커맨드 드라이버**(`targets`/`eval`/`key`/`type`/`mouse`/`shot`)를 만들어 인라인 코드 실행을 아예 없앤다. 파일 쓰기·셸 실행 같은 부수효과는 드라이버에 넣지 않는다(임의 코드 실행 개방 금지 — 권한 규칙도 이 도구 하나만 좁게 허용). `--focus` 플래그를 내장해 §3.5 포커스 에뮬레이션을 옵션 하나로 켤 수 있게 한다.
```
cdp.py targets --port 9224
cdp.py eval  --port 9224 --title <탭식별> --focus --expr "document.title"
cdp.py key   --port 9224 --title <탭식별> --focus --key Backspace
cdp.py mouse --port 9224 --title <탭식별> --focus --seq '[["press",x,y],["move",x2,y2],["release",x2,y2]]'
```
같은 명령을 도구 하나로 좁혀 반복 실행해도 더는 분류기에 걸리지 않았다(도입 후 재발 0).

### 5. 다이얼로그·네비게이션 안전
- **`beforeunload` 다이얼로그 자동 처리 의무**: 미저장 편집이 남은 탭을 navigate하면 "나가시겠습니까" 모달이 **오너 화면**에 뜬다(포커스 탈취와 같은 계열의 피해 — 오너가 직접 눌러 치워야 함). `Page.javascriptDialogOpening` 구독 + `Page.handleJavaScriptDialog {accept:true}` 등록을 navigate 전에 반드시 걸고, 가능하면 navigate 전에 저장까지 기다린다.
- **CDP 무응답 ≠ 데드락**: `evaluate`가 응답 없어 보인다고 곧바로 렌더러 데드락으로 단정하지 마라 — 탭이 HTTP 5xx 오류 페이지 등에 물려 있을 수 있다. 먼저 그 탭의 **title/URL부터 확인**하고, 그래도 진짜 무응답이면 데드락으로 판정한다(브라우저/페이지 두 레벨 모두 재확인 후 판정 — [[pipelines.00-campaign-kickoff-playbook]] §3 참고).

## 적용 체크리스트

- [ ] 브리프/정책에 "포커스 탈취 금지" 명문화 (워커는 새 컨텍스트라 매번 읽어야 함)
- [ ] 클론 작업 전체 → **headless 기본**(표준 런치 헬퍼 경유, 손 launch 금지)
- [ ] 헬퍼가 dpr/스크린샷 실폭 자기검증하는지 확인(half-res 조용한 실패 차단)
- [ ] **실물 로그인 세션 창에서 키/캐럿/클립보드 조작이 필요하면 포커스 에뮬레이션**(§3.5) — headless로 대체 시도하지 말 것(세션 없음)
- [ ] 새 탭 필요 시 `Target.createTarget(background:true)` + 종료 시 정리
- [ ] osascript가 필요한 시나리오는 별도 표시 + 사전 승인
- [ ] 실측 스크립트는 인라인 `python -c` 대신 **전용 CDP 드라이버**(§4) 서브커맨드로
- [ ] 드래그·마퀴 재현은 매 `mousemove`에 `buttons` 필드 명시(§3.6)
- [ ] navigate 전 `Page.javascriptDialogOpening` 구독 등록(§5)

## 크로스캠페인 정본

이 규칙은 clone-kb `PROTOCOL.md` §2.5(크로스캠페인 운영 결정, append-only)에도 등재돼 **모든 클론 세션에 즉시 적용**된다. 캠페인 리포의 `_POLICY.md`는 이 카드를 프로젝트값(포트·경로)으로 구체화한 사본이다([[pipelines.02-campaign-policy-standard]]).

## 실증

- **★최대 성과(2026-07-20, notion)**: 포커스 에뮬레이션(§3.5) 도입 전 3회 연속 실패하던 실물 키입력 재현이 도입 직후 24/24 전량 성공. 근거: 260622_notion-clone 리포(private) 커밋 a1d2ec8("배경 창 visibilityState hidden 해소 — CDP 포커스 에뮬레이션, fn-delete 3회 실패의 근본 원인") + `harness/cdp.py`·`harness/fwddel5_lib.py`(둘 다 `Emulation.setFocusEmulationEnabled`+`Page.setWebLifecycleState` 사용).
- **★실측 정정(2026-07-20, notion W-FH)**: "백그라운드 탭에도 키가 전달된다"는 통념은 **틀렸다** — 공유 headful 브라우저에서 비활성 탭의 `Input.dispatchKeyEvent`는 드롭된다. 마우스·계측·캡처는 백그라운드에서 정상이지만 **키 입력이 필요한 재현/영상은 단명 headless launch 또는 포커스 에뮬레이션이 안전한 경로**다(대상에 따라 §3 vs §3.5).
- **notion(2026-07-20)**: 오너 3회 호소 → 정책 §브라우저에 금지 규칙 + 역할 분리 확립, 가동 중 워커 2명에 즉시 주입. 이후 계측·게이트·재현은 전부 백그라운드로 수행 가능함을 확인.
- **전용 CDP 드라이버(§4)**: 도입 전 하루 4회 세션 안전 분류기 오탐 → 도입 후(`harness/cdp.py`) 재발 0.
