# PLAYBOOK — 클론 캠페인 진입 플레이북

> **새 클론 캠페인을 시작하는 세션이 가장 먼저 로드하는 문서.** "어떤 순서로 클론하나(방법 선택) · 과거에 어떤 삽질을 했나(시행착오) · 방법론이 어떻게 여기까지 왔나(진화)" 세 가지를 하나로 묶는다. 기법 자체의 정의·근거는 각 `techniques/*.md` 카드에 있다 — 이 문서는 그 카드들을 **엮는 지도**이지 재작성이 아니다.
>
> **이 문서와 [[pipelines.00-campaign-kickoff-playbook]]의 관계**: 그 문서는 "복붙용 체크리스트 + 3질문 + 실수 표"로 빠르게 훑는 압축판이다. 이 문서는 그것을 감싸는 상위 서사 — *왜* 그 순서인지, *왜* 그 실수가 났는지, *어떻게* 지금 형태로 진화했는지를 설명한다. 실행 직전엔 00번 체크리스트로, 판단이 필요할 땐 이 문서로.

updated: 2026-07-18 · owner: 박춘순

---

## 0. 3캠페인 스냅샷 (이 플레이북의 근거 데이터)

| 캠페인 | 유형 | 시작 방식 | 현재 방법론 축 | 상태 |
|---|---|---|---|---|
| [[cases.notion]] | 문서형 (DOM 골격이 본체) | 스타일-먼저 → 7이터레이션 대가로 구조-우선 원칙 발견 | structure-first 원산지 | RIP P0~P3 완료, API 파리티 루프 paused |
| [[cases.canvas]] | 캔버스형 (노드그래프+생성 파이프라인) | 세션1~20 스타일-먼저 누적 → 세션21 retrofit | total-fidelity(B) 채택, 11차원 매트릭스 진행 중 | 세션22, attribute-diff 17,113 |
| [[cases.akiflow]] | 목록·일정형 | 처음부터 kit 표준 적용 | port+profile 격리·gate.py 3축의 원 사례 | M0 정찰 완료 후 일시정지 |

---

## 1부 — 방법 선택 가이드 (새 타깃을 만나면 무엇부터)

### 1.0 결정 포인트 먼저 (아키텍처를 가르는 질문)

| 질문 | Yes | No |
|---|---|---|
| **대상 유형이 뭔가** | 문서형(notion류) → DOM 골격 = 본체, 구조-우선이 절대 1순위 | 캔버스형(canvas류) → 골격+상태머신+데이터모델(클립보드/좌표계) 셋 다 본체 |
| **실물 접근이 CDP로 되나** | 된다 → [[techniques.cdp-nondestructive-recon]](peek 패턴)이 전 단계의 토대. 로그인 세션 있는 실사용 계정이면 [[techniques.port-profile-isolation]] 먼저 | 로그인 불가/사용 제한이면 정찰 범위를 read-only 캡처 자산으로 제한하고 정찰 단계를 늘려 잡는다 |
| **이미 스타일-먼저로 몇 세션 진행됐나** | 그렇다(레거시 존재) → §1.7 retrofit 경로. 처음부터 다시 안 함 | 아니다(신규 착수) → §1.1부터 순서대로, retrofit 불필요 |
| **캠페인이 웹앱(문서/캔버스)이냐 노드캔버스형 클립보드 앱이냐** | 노드캔버스형이면 [[techniques.canvas-clipboard-localstorage]] 크로스툴 가설부터 검증(OS클립보드=마커, payload=localStorage 패턴이 이 앱에도 있나) — 있으면 [[techniques.canvas-coord-inject-rearrange]]까지 재사용 가능 | 일반 문서형 웹앱이면 클립보드 조사는 건너뛰고 API 계약 파리티(§1.4) 쪽에 무게 |

북극성 질문("완료를 무엇으로 검사하는가")과 3질문 합의는 [[pipelines.00-campaign-kickoff-playbook]] §0을 그대로 쓴다(중복 서술 안 함) — 이 플레이북은 그 답이 나온 **다음**부터 시작한다.

### 1.1 ①정찰 (recon) — read-only, 신규 캡처 최소화

- **기법**: [[techniques.cdp-nondestructive-recon]](peek, 리로드 금지) · [[techniques.cdp-raw-driver]](좀비 탭 우회, Playwright connect_over_cdp가 행업될 때) · [[techniques.port-profile-isolation]](프로젝트당 전용 포트+프로필) · [[techniques.clone-documentation-formats]](정찰 단계는 인터랙션 인벤토리 → 유저/스크린 플로우 → 결정표 순으로 원자재 확보)
- **하네스**: `peek.py`(shot/dom/tokens/probe/click 서브커맨드) 계열, 3캠페인 공통 패턴
- **exit gate**: 원자재 확보(스샷+DOM+토큰 최소 1세트) + 안전경계 문서화(무엇이 read-only이고 무엇이 개방됐는지 최신 오너 지시 반영 — §2 도그마 함정 참고) + 포트/프로필 배정 완료
- **함정 주의**: "read-only"가 "클릭 금지"로 과잉 확대되면 지연마운트 UI(호버 툴바 등)를 통째로 놓친다 — §2의 도그마 사고 참고
- **★정찰 초반에 DOM vs WebGL 렌더 판별부터**(canvas 2026-07-18 발견 이후 표준): 노드/컴포넌트가 캔버스에 픽셀로 렌더될 수 있는 앱(Figma·Miro류 하이브리드)이면 구조 추출(§1.2)로 넘어가기 전에 3-신호로 판별 — ①뷰포트 전체 크기 `<canvas>`+`getContext('webgl')` 성공 ②노드 컨테이너(`.react-flow__nodes`류) children 0 ③노드 텍스트가 `document.body.innerText`에 부재. 3개 다 참이면 해당 층은 WebGL 렌더로 확정 → [[techniques.webgl-node-rendering-clone]] 경로로 전환(§1.2의 골격-우선 대신 data-model+visual+behavior 캡처, [[techniques.coordinate-click-capture]]로 인터랙션). 셸/툴바/인스펙터/메뉴는 이 판별과 무관하게 여전히 DOM일 수 있으니 부분별로 판별한다.

### 1.2 ②구조 추출 (skeleton) — 무조건 1순위

- **기법**: [[techniques.structure-first-cloning]](①골격→②스타일→③동작 순서, 오너 1순위 채택 원칙) · [[techniques.total-fidelity-cloning]](B원칙 — 골격을 잎↔부모뿐 아니라 셸까지 1:1, 11차원 중 ①번) · [[techniques.dom-first-measurement]](픽셀 대신 DOM+computedStyle을 1차 오라클로) · [[techniques.rip-css-dump]](RIP 레이어① 전수 덤프)
- **하네스**: `rip_chain.py`(잎→root 조상체인 전 층 덤프), `dom_snap.py`/`dom_recorder.py`
- **exit gate**: 구조 게이트 — 태그·a11y role·부모-자식 그룹핑(마커+텍스트 단일 부모류)·래퍼 체인이 실물과 0 미스매치. 셸(body까지)은 공통 조상이라 1회 추출로 끝
- **원칙**: 골격이 같아야 스타일이 "보정 없이" 공짜로 따라온다 — 이 순서를 건너뛰면 §2 최대 실수를 반복한다

### 1.3 ③스타일 포팅 — 골격 확정 후에만

- **기법**: [[techniques.dom-first-measurement]]로 실측한 computed 값을 골격이 같은 노드에 그대로 이식 (전담 카드 `measured-css-porting`은 아직 미작성 — [[techniques.measured-css-porting]]로 마커만 남겨둠, 다음 카드화 후보)
- **exit gate**: attribute-diff 카운트가 수렴 방향으로 감소([[pipelines.99-percent]] 축), 보정 스택(A의 오차를 B의 마진으로 상쇄) 흔적 없음

### 1.4 ④상태·동작 지도 — 상태 매트릭스 + 이벤트 리스너 지도

- **기법**: [[techniques.interaction-state-map]](노드/컴포넌트 전 버튼→상태 말단까지, 상태전이+매트릭스+갤러리 3종 1문서) · [[techniques.state-explorer]](아직 못 본 상태를 도구가 자동 발견, 커버리지 %) · [[techniques.state-spec-json]](URL+도달절차를 real/clone 병렬 JSON으로 재현 가능하게) · [[techniques.rip-crawler]](RIP 레이어② 인터랙션 크롤러) · [[techniques.total-fidelity-cloning]] 11차원 중 ③상태머신(전이 **메커니즘 분류**까지 — mount/unmount인지 opacity토글인지)·④데이터모델(클립보드/직렬화 계약)
- **하네스**: `rip_state_diff.py`(경로 diff, 마운트/언마운트/스타일변경 3분류), `gen_map.py`(STATES 리스트 하나로 다이어그램+표+갤러리 자동 파생)
- **exit gate**: 상태 커버리지 ≥95%([[pipelines.99-percent]] 항목①), 전이 메커니즘까지 실물과 동일 분류(B 원칙 적용 시)

### 1.5 ⑤검증 게이트 — 빌더 자가선언 불신

- **기법**: [[techniques.adversarial-verification]](빌더≠검증자, verify-first) · [[techniques.orchestrator-model-routing]](검증자 모델 ≥ 빌더 모델) · [[techniques.regression-harness-suite]](번호매김 `_bN_verify.py`/`*_gate.py`) · [[techniques.rip-repair-loop]](델타→티켓→재덤프 수렴 루프) · [[techniques.model-matrix-diff]](카탈로그 전수 검증, 크레딧 0) · [[techniques.visual-triage-sheet]](사람 판독용 bbox 오버레이) · 픽셀 배지 전담 카드는 아직 미작성 — [[techniques.pixel-diff-baseline]]으로 마커만
- **exit gate**: 구조 게이트 + 픽셀/속성 배지 + 기능 게이트 **3축이 항상 쌍으로** 통과(하나만 통과시켜 "완료" 선언 금지 — §2 최대 실수의 재발방지 규칙)

### 1.6 ⑥인수인계 (handoff)

- **기법**: [[techniques.interaction-state-map]](화면이 먼저 보여야 새 합류자가 빠르다) · [[techniques.clone-documentation-formats]](정찰/구조/상태/검증/인수인계 5단계 포맷 매핑, 인수인계는 인터랙션 상태지도→와이어플로우→저니맵 순) · [[techniques.append-only-logging]](워크로그·티켓·갭매트릭스 append-only) · `cases/<캠페인>.md`(루프 도식+진행단계 mermaid) · `status/<캠페인>.md`(라이브 상태판)
- **exit gate**: `cases/<캠페인>.md` 갱신 + 이 KB에 신규/승격 기법 기록 + 아침 보고 HTML(무인 런이었다면, [[techniques.night-run-sop]]·PROTOCOL.md §2 형식)

### 1.7 이미 스타일-먼저로 진행된 캠페인 — retrofit 경로

처음부터 다시 하지 않는다. [[techniques.structure-first-cloning]] §실증2(canvas 세션21)가 실측한 절차:

1. **정찰 우선, 신규 캡처 없이** — 기존 델타 문서 + 서술형 RECON + 현재 소스코드(git log/grep) 3축 교차검증만으로 "진짜 구조 갭"을 추려낸다(스테일 항목·하네스 오탐부터 먼저 걸러냄).
2. **블록 단위 점진 리트로핏** — 리스크 낮은 것(신규 섹션 추가류)부터, 렌더러 심장부(입력 골격 등)는 게이트망 선행 후 마지막. 매 블록마다 무회귀 재확인 후 다음 블록.
3. **이미 검증된 패턴 재사용** — 다른 컴포넌트에서 프로덕션 검증된 패턴(canvas의 `useEditableSeed`)을 재사용하면 심장부급 리팩터도 신규 리스크 없이 확산 가능.

실측 결과: 헤더span 1건이 6상태 diff -40%, 라이트박스 1건이 -29% 동반 감소 — "구조 정합 1건이 스타일 레이어 다수를 공짜로 데려온다"는 메커니즘이 신규 설계 캠페인(notion)과 레거시 retrofit 캠페인(canvas) 양쪽에서 재현됨.

### 1.8 그 다음 — 전층 계약까지 (B 원칙, total-fidelity)

가시·상호작용 층 99%에 도달한 뒤에도 "픽셀·기능이 등가"라는 이유로 골격 층수·상태 메커니즘·데이터 계약 차이를 "무해 단순화"로 절충하지 않는다 — [[techniques.total-fidelity-cloning]] 11차원 표를 열어 ○/△/✗ 각 차원을 확인. **빌더·검증자가 픽셀 등가를 근거로 골격/메커니즘 차이를 스스로 "무해"라 닫지 말 것** — 오너 승인 전까지는 열린 항목으로 취급한다.

---

## 2부 — 시행착오 카탈로그 (증상 → 원인 → 교훈 → 재발방지)

같은 돈을 두 번 내지 않기 위한 실전 사고 기록. 순서는 발생/발견 시점 대략순.

### ① 스타일-먼저로 출발한 것 자체가 최대 실수 — [[techniques.structure-first-cloning]]
- **증상**: computed 값(색상·크기·여백)을 요소 단위로 포팅하며 픽셀 겹침을 91%→96%까지 끌어올렸다.
- **원인**: 골격(태그·role·부모-자식 그룹핑) 확인 없이 스타일 값부터 맞췄다 — 서로 다른 골격의 오차를 인접 요소 마진으로 상쇄하는 "보정 스택"이 쌓였다.
- **교훈**: 오너가 DevTools로 직접 요소를 인스펙션하니 제목(태그/role/패딩축), 리스트(마커·텍스트 부모 분리), 거터(이중예약), 테이블(보더 층), 래퍼 체인까지 **골격이 사실상 전부 불일치**였다. 보정 스택은 특정 상태에선 픽셀이 맞아도 내용이 바뀌면 깨진다(번호목록 높이 붕괴로 실제 발현).
- **재발방지**: 구조-우선(①골격→②스타일→③동작)이 모든 캠페인의 무조건 1순위. 골격 리팩터는 렌더러 심장부를 건드리므로 게이트망 선행 + 블록 단위 점진. 이미 스타일-먼저로 진행된 캠페인은 §1.7 retrofit.

### ② 픽셀 지표가 준 거짓 안심 — [[techniques.structure-first-cloning]]
- **증상**: 픽셀 diff 배지가 96%까지 수렴해 "거의 다 됐다"고 판단할 뻔했다.
- **원인**: 골격 게이트 없이 픽셀 수치만 단독 오라클로 썼다 — 보정 스택이 상쇄한 결과를 "일치"로 오보고.
- **교훈**: **픽셀 지표가 높다 ≠ 복사가 됐다.** 골격 검사 없는 픽셀 지표는 거짓 안심이다. 두더지잡기 7이터레이션 + 골격 전면 retrofit 비용을 낸 뒤에야 이 사실이 드러났다.
- **재발방지**: 픽셀 배지는 반드시 구조 게이트와 **쌍으로만** 신뢰한다. 한쪽만 통과시켜 "완료" 선언 금지(§1.5 검증 게이트 exit 조건).

### ③ read-only/GENERATE 금지 도그마가 오너 개방 지시를 덮어씀 — [[techniques.cdp-nondestructive-recon]]
- **증상**: 오너가 2026-07-14 "우리 클론 R&D는 전부 redo 가능하니 파괴적 조작·GENERATE 모두 허용"으로 전면 개방했는데도, 문서에 남은 낡은 "실측 불가/read-only" 조항 때문에 지연마운트 UI 실측을 포기하고 그 공백을 워커가 자작 자산으로 메꾸는 사고(notion 아이콘 자작)가 났다.
- **원인**: 개방 지시가 떨어졌을 때 관련 문서 전체의 잔존 조항을 즉시 소거하지 않았다 — 낡은 조항이 최신 오너 지시보다 우선 적용되는 구조적 결함.
- **교훈**: "실측 불가" 선언 전에 반드시 3단 체크 — ①기술적으로 불가한가 ②정책상 불가한가 ③그 정책이 최신 오너 지시와 일치하는가. ③이 항상 최우선.
- **재발방지**: 개방/정책 변경 지시는 받는 즉시 모든 관련 문서(카드·브리프·SOP)의 잔존 조항을 소거. 진짜 금지는 **비가역·외부유출뿐**(외부전송·게시·결제·영구삭제·계정변경) — 그 외엔 실측을 도그마로 포기하지 않는다.

### ④ 멀티탭 CDP substring 매칭 충돌 → 실제 데이터 손상 — [[techniques.cdp-raw-driver]]
- **증상**: 같은 dev 포트(`localhost:5175`)에 탭이 2개 이상 열려 있던 상태에서, 빌더 세션이 `url_substr` 매칭으로 엉뚱한(오래된/다른 프로젝트) 탭에 attach — 클론 자율생성 프로젝트(`doc.json`)를 빈 상태로 **2회 오토세이브 덮어씀**.
- **원인**: "부분 문자열 포함하는 첫 healthy 타겟"을 잡는 매칭 방식이 다중 탭 상황에서 비결정적이었다.
- **교훈**: 백업에서 즉시 복원해 데이터 유실은 없었지만, 발견이 늦었으면 산출물이 조용히 사라질 뻔했다.
- **재발방지**: 다중 매칭 시 조용히 첫 번째를 고르지 않고 **즉시 시끄럽게 실패**(에러 raise, 후보 목록 출력)하도록 `CdpSession` 초기화 로직에 가드 신설. 운용 규칙: 무인 런에서는 탭당 1빌더·canvas-id 등으로 고정해 애초에 모호성이 생길 상황을 피한다(크로스캠페인 결정, PROTOCOL.md §2.5).

### ⑤ 크레딧 추정치를 믿었다가 헛경보 — [[techniques.model-matrix-diff]]
- **증상**: registry 표시 비용(예: seedance 18cr)이 실측(17.5cr)과 어긋났고, 빌더의 bridge-history 추정은 실제 17.5cr을 ~70cr급으로 오산했다. 세션 중간 체크포인트를 시작 잔액으로 오인하는 사고도 별개로 발생.
- **원인**: 크레딧 판단을 registry 표시값·빌더 추정치·오케 브리핑 문구 자체에 의존했다.
- **교훈**: 표시값은 카탈로그 정합 검증용으로만 쓰고, **실제 비용 판단(모델 선택·예산 산정)은 반드시 MCP `balance`/`transactions`로 확정**해야 한다.
- **재발방지**: 크로스캠페인 결정(PROTOCOL.md §2.5) — 크레딧 정본은 MCP 거래내역만. "시작 잔액 = 직전 런의 종료 잔액(status/ 기록)과 일치하는지"부터 먼저 검증하는 절차를 무인 런 셋업 단계에 명문화.

### ⑥ 서브에이전트 스폰 후 백그라운드 통지 대기로 산출물 유실 — [[techniques.night-run-sop]] · [[techniques.subagent-fanout-rules]]
- **증상**: 워커가 백그라운드 알림을 기다리며 결과를 저장하지 않고 턴을 끝낸 사고(2026-07-11/12, "산출물 0·규칙위반"). 브리프에 금지 문구를 명문화한 뒤에도 세션16(2026-07-15)에서 "통지 대기" 정지가 **2회 재발**(P9) — 오케가 SendMessage로 개입해야 풀렸다.
- **원인**: 판단이 필요 없는 결정적 작업까지 서브에이전트에 위임하고, 그 에이전트가 스폰 후 알림을 기다리는 패턴 자체가 무인 런에서 정지점이 된다. [[techniques.subagent-fanout-rules]]의 5조 규칙("결정적 작업은 스크립트, 판단 필요만 에이전트")을 어긴 경우 특히 심하다.
- **교훈**: 브리프 명문화만으로는 재발을 못 막는다 — 반복되면 코드 레벨 강제가 필요하다.
- **재발방지**: "백그라운드 알림 대기 없이 결과 즉시 저장"을 워커 프롬프트 필수 문구로. 통지 대기는 bounded 폴링으로 대체(무한 대기 금지). 반복 재발 시 night-run-sop 코드 레벨 강제(타임아웃+오케 개입)로 격상.

### ⑦ 공유 실시간 캔버스에서 결과 노드가 원인 불명으로 소실 — [[techniques.interaction-state-map]]
- **증상**: REC-B 세션(2026-07-11)에서 완료 결과 노드의 "Expand view"(라이트박스 열기) 버튼을 클릭한 직후, 공유 실시간 캔버스의 결과 노드 1개가 원인 불명으로 사라졌다.
- **원인**: 미확정(인시던트 원인 자체가 규명 안 됨) — 다만 실시간 동기화되는 **공유 문서**에서 발생했다는 조건은 확정.
- **교훈**: "결과 상태는 read-only 관측"이 "절대 클릭 금지"를 뜻하지는 않지만, 실시간 공유 문서에서의 조작은 인시던트 재현 없이도 실물 손실로 이어질 수 있다.
- **재발방지**: 이후 그 버튼은 재클릭 금지로 남았다가, 후속 세션이 **디스포저블(희생 가능) 샌드박스**에서 3회 재시도해 미재현을 확인하고서야 안전하게 재확보했다. 규칙: (a) 실시간 공유 문서가 아니라 디스포저블 샌드박스에서, (b) 클릭 직후 즉시 노드 수 카운트+스크린샷 비교로 이상 유무 확인, (c) 과거 인시던트가 있던 액션은 재시도 전 그 기록부터 읽는다. 성숙한 캠페인에서는 "또 클릭해서 재확인"보다 이미 검증된 기존 캡처를 인용하는 편이 더 안전하다.

### ⑧ 클립보드가 "서버로 갔다"는 오진단 — 실제는 로컬 localStorage — [[techniques.canvas-clipboard-localstorage]]
- **증상**: Cmd+C 직후 OS 클립보드(`pbpaste`)를 보니 UUID/토큰처럼 짧은 문자열뿐이라 "서버 어딘가에 저장되고 이건 참조 ID인가보다"로 넘겨짚었다.
- **원인**: OS 클립보드만 보고 판단했다 — 실제 그래프 payload는 `localStorage['higgsfield-canvas-clipboard']`에 `{marker, payload}` 형태로 저장되고, Cmd+C~V 전 구간 네트워크 요청은 0건(서버 왕복 없음)이었다.
- **교훈**: 4일 전부터 동일했던 로컬 2단 구조였음이 재확인됐다 — "서버 참조인가보다"는 검증 없는 추측이었다.
- **재발방지**: "복사한 데이터가 대체 어디 있나"를 찾을 땐 서버로 넘겨짚지 말고 **로컬(localStorage/IndexedDB)부터 먼저 덤프**. 확정하려면 음성대조(negative control — 로컬 페이로드만 삭제 후 붙여넣기 실패 확인)와 정적 소스 grep(`fetch(`/`/api/` 유무)까지 3중 증거로 닫는다.

### ⑨ 컴퓨터가 잠들어(macOS sleep) 무인 런이 중단됨 — [[techniques.night-run-sop]]
- **증상**: 세션13(2026-07-14) 장시간 무인 런 도중 컴퓨터가 시스템 잠자기(sleep) 상태로 들어가며 게이트가 중단됐다. 빌더 산출물은 커밋으로 안전했지만 게이트 재실행 비용이 발생.
- **원인**: 무인 런 셋업 단계에서 시스템 잠자기 방지 조치를 하지 않았다.
- **교훈**: 무한 재시도·sleep 루프뿐 아니라 **OS 레벨 sleep도 야간 런을 죽이는 원인**이다 — 애플리케이션 로직과 무관한 인프라 층 실패.
- **재발방지**: 세션16(2026-07-15)부터 무인 런 셋업에 `caffeinate`로 잠자기 차단을 표준 포함(PID 기록까지) — 10시간 런이 중단 없이 완주됨. 이후 재발 없음.

### 부록 — localStorage 레이스로 인한 상태 리셋 ("away-클로버" 사고) — [[techniques.atomic-localstorage-inject]]
- **증상**: 템플릿마다 write→reload를 반복하는 방식(`build_t2.py`)이 유휴 세션 중 레이스를 일으켜 클론이 이전 20-DB 상태로 조용히 리셋됐다(2026-06-27).
- **원인**: localStorage 자체엔 트랜잭션이 없다 — 여러 write 사이에 reload/다른 스크립트의 write가 끼어들면 마지막에 이긴 쪽만 남는다.
- **재발방지**: 모든 소스를 메모리에서 합친 뒤 **단 한 번의 write + 단 한 번의 reload**로 끝낸다(`bulk_inject.py`). 대상 탭 포트를 코드 레벨에서 재확인하는 정규식 가드(`CLONE_TAB_RE`)도 병행.

---

## 3부 — 방법론 진화 (무엇을 지불하고 무엇을 배웠나)

시간순 타임라인. 각 단계가 **무엇을 지불했고 무엇을 남겼는지**를 축으로 정리.

### 1단계 — notion: RIP 3단·osascript·구조-우선 원칙의 발원지 (2026-06 하순 ~ 07-13)
- **지불**: 스타일-먼저로 91%→96% 픽셀 수렴까지 갔다가 오너 DevTools 인스펙션에서 골격이 사실상 전부 불일치임이 드러남 — 7이터레이션 + 골격 전면 retrofit 비용(§2-①). CDP untrusted 입력으로 노션 슬래시 메뉴가 3회 연속 실패(B4).
- **배움**: [[techniques.structure-first-cloning]] 원칙이 이 대가에서 결정화됨 — "골격이 같으면 스타일은 거의 공짜"라는 인과가 여기서 처음 실증됨. B4는 [[techniques.osascript-trusted-hybrid]](2026-06-26 돌파, CDP는 포커스·캐럿·캡처만/실제 키입력만 osascript로 전환, 한글은 클립보드 붙여넣기로 IME 우회)로 해결.
- **남긴 것**: [[techniques.dom-first-measurement]]·[[techniques.pixel-screenshot-as-primary-oracle]](은퇴, 2026-07-10 canvas와 같은 날 독립 채택) · [[techniques.adversarial-verification]](`ci_agent`+`ci_compare` 동일 오라클 이중 실행) · [[techniques.atomic-localstorage-inject]](away-클로버 사고 이후) · [[techniques.state-spec-json]].

### 2단계 — canvas: 20세션 스타일-먼저 누적 → 세션21 retrofit → 세션22 B결정 (07-13 ~ 07-17)
- **지불**: 세션1~20을 스타일-먼저(값 포팅) 방식으로 누적 진행 — notion의 교훈이 있었음에도 캔버스형(노드그래프) 앱은 별도로 같은 함정을 다시 밟았다. attribute-diff가 38,476까지 쌓였다가 여러 세션에 걸쳐 소탕(30,580→23,581→17,490→17,113).
- **배움 — retrofit이 탈출 경로임을 실증(세션21)**: 처음부터 다시 하지 않고 §1.7 절차(정찰 우선·블록 단위 점진·검증된 패턴 재사용)로 소급 적용. 헤더span -40%, 라이트박스메타패널 -29% 동반 감소로 "구조 정합이 스타일 레이어를 공짜로 데려온다"는 메커니즘이 별개 앱·별개 프레임워크(@xyflow)에서도 재현됨을 확인.
- **배움 — 그 다음이 더 있었다(세션22)**: 스켈레톤 매트릭스가 체인 층수 격차(real13 vs clone10)·상태전이 메커니즘 격차(mount/unmount+reflow vs opacity토글)를 "최종 픽셀 등가라 무해"로 자체 판정했으나, 오너가 결산 시점에 개입해 뒤집었다 — "프로들이 그 층 구조를 이유있게 만들었고, 층까지 맞춰야 실물이 기능을 추가해도 클론이 따라갈 수 있다." A안(픽셀/기능 등가로 절충)을 기각하고 B안(전층 일치)을 채택 — [[techniques.total-fidelity-cloning]] 신설, 11차원 매트릭스로 "무해 단순화"를 재분류 대상으로 다시 열었다.
- **남긴 것**: RIP 3단 파이프라인([[techniques.rip-css-dump]]·[[techniques.rip-crawler]]·[[techniques.rip-repair-loop]]) · [[techniques.cdp-raw-driver]](좀비 탭 우회, 이후 멀티탭 데이터손상 가드까지) · [[techniques.model-matrix-diff]] · [[techniques.dogfooding-as-bug-discovery]](BORI 실사용 6버그) · [[techniques.orchestrator-model-routing]] · [[pipelines.99-percent]] · [[techniques.cross-paste-parity]] · [[techniques.canvas-clipboard-localstorage]] · [[techniques.canvas-coord-inject-rearrange]](세션20, T1~T5 5/5 실증으로 verified 승격) · [[techniques.structure-first-cloning]] retrofit 실증 · [[techniques.total-fidelity-cloning]](B원칙).

### 3단계 — akiflow: 표준 이식 대상, 격리·게이트 패턴의 원 사례
- **지불**: 다른 두 캠페인보다 활동은 적었지만(M0 정찰 후 일시정지), 실시간 협업 기능 확인 불가 등 실물 제약(B1/B2/B7)을 먼저 만나 "측정 불가한 상태는 억지로 만들지 않는다"는 절제를 실증.
- **배움**: 클론 캠페인 세 번째부터는 신규 기법을 발명하기보다 **기존 표준을 그대로 이식**하는 비중이 커진다 — 포트/프로필 조합(9222/5180)이 이후 canvas(9223/5175)·notion(9224/5185) 배정의 기준점이 됨.
- **남긴 것**: [[techniques.port-profile-isolation]](원 사례) · [[techniques.regression-harness-suite]]의 진화형(`gate.py` 3축 통합 게이트) · [[pipelines.night-run]](cmux 오케스트레이터 킥오프가 vault SSOT를 그대로 채택).

### 4단계 — 문서화 신기법: "텍스트만이면 안 와닿는다" (2026-07-17)
- **지불**: 캠페인이 22세션까지 길어지면서 정찰 산출물 형태가 세션마다 제각각(서술만/표만/스샷만)이 됐다. 오너가 직접 지적: "텍스트만이면 안 와닿는다 — 각 포맷을 실제 예시로 보여줘."
- **배움**: 포맷 선택 자체가 정찰 품질에 영향을 준다는 것 — "스샷+구조화 표+mermaid 다이어그램" 조합이 AI/사람 공통 판독에 가장 좋다는 것이 실증적으로 확인됨.
- **남긴 것**: [[techniques.interaction-state-map]](상태전이+매트릭스+갤러리 3종을 STATES 리스트 하나에서 자동 파생하는 `gen_map.py` 패턴, canvas 이미지 Generate 노드 파일럿 21상태를 신규 CDP 조작 0건·기존 캡처 재사용만으로 완성) · [[techniques.clone-documentation-formats]](16개 업계 포맷을 정찰/구조/상태/검증/인수인계 5단계에 매핑하는 카탈로그, AI 소비용 규율 — 표보다 JSON/path-diff가 게이트엔 낫다는 원칙 포함).

### 누적 원칙 (지금 이 시점의 결론)
1. 골격이 먼저다 — 예외 없음. 픽셀 지표는 구조 게이트 없이 단독으로 신뢰하지 않는다.
2. 완료 판단은 자가선언이 아니라 재측정(적대적 검증)과 디스크 산출물로만.
3. 크레딧·비용은 MCP 거래내역만 정본, 어떤 추정치도 정본이 아니다.
4. 무인 런은 "막히면 우아하게 skip"이 원칙이지, 멈추거나 무한 재시도하지 않는다 — sleep(시스템/통지대기) 둘 다 인프라 층에서 킬러가 될 수 있음을 기억한다.
5. 좋은 방법은 반드시 이 KB에 들어와야 다음 캠페인이 로드해서 쓴다 — 카드로 안 남으면 다음 캠페인이 같은 대가를 다시 치른다.

---

## 소비 방법

1. 신규 캠페인 첫 세션: 이 문서 → §0 스냅샷으로 선례 확인 → §1로 방법 순서 결정 → 관련 기법 카드만 `index.md`에서 로드.
2. 판단이 갈리는 순간(스타일-먼저로 갈지, retrofit할지, 도그마를 깰지): §2 시행착오에서 유사 사례부터 찾는다.
3. "이 방법이 왜 지금 이 형태인가"가 궁금할 때: §3 진화 타임라인.
4. 새로 겪은 시행착오나 새 기법은 이 문서에 append하지 않는다 — 해당 `techniques/*.md` 카드 또는 `runs/`에 먼저 기록하고, 그 카드가 검증(verified 이상)되면 이 플레이북 §2/§3에 요약을 추가한다(정본은 항상 카드, 이 문서는 파생 지도).

### 정상 운영(steady-state) 원칙 — 베이스라인-후-diff (canvas 2026-07-18)

캠페인이 §1.6 인수인계까지 한 바퀴 돌고 나면, 매 세션을 처음부터 다시 서베이하지 않는다. [[techniques.baseline-then-diff]]가 이 국면의 관리 원칙: **베이스라인은 한 번만 전수**(모든 상태·모든 스크린샷), 그 이후는 [[techniques.version-archive-3layer]]로 자동 아카이브(월 1회, MHTML+PNG+localStorage 3층)를 돌리며 **변경분만 diff**한다. 판단 기준은 "이 변화가 방법론/엔진베이스에 기여하나?" — 기능/구조 변화만 클론에 반영하고, 순수 시각 리스타일은 아카이브만 하고 쫓지 않는다(러닝머신 방지). 데이터모델·방법론·하네스 코드·오너 결정은 **durable**로 계속 관리하고, 스크린샷·UI 레이아웃·모델 목록 같은 **snapshot**은 날짜를 찍고 동결한다 — element map은 그 날짜 시점 학습 자료이지 실물의 라이브 미러가 아니다.
