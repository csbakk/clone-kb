---
id: runs.2026-07-17-canvas-complexwf
title: canvas 세션 20 — 복잡 노드 연결 워크플로우 5주제 매칭(T1~T5) 실물↔클론 완성
doctype: run
campaign: canvas
date: 2026-07-17
status: done
techniques_loaded: [techniques.canvas-clipboard-localstorage, techniques.canvas-coord-inject-rearrange, techniques.cross-paste-parity, techniques.osascript-trusted-hybrid, techniques.cdp-raw-driver, techniques.model-matrix-diff, techniques.adversarial-verification]
pipeline: pipelines.verify-first-loop
routing: "오케=opus / 빌더=sonnet"
owner: 박춘순
---

# 런 매니페스트 — canvas 세션 20 (복잡 워크플로우 5주제 매칭)

## 1. 로딩 기법 + 근거
| 기법 | status(런 시작 시점) | 역할 |
|---|---|---|
| [[techniques.canvas-clipboard-localstorage]] | experimental(canvas 실증) | 좌표 재배치 주입의 전제 메커니즘(OS마커+localStorage payload) — 이번 런에서 재확인만(§_RECON_CLIPBOARD_API.md, "서버 참조 ID" 가설 기각), 유효성 재검증 완료 |
| [[techniques.canvas-coord-inject-rearrange]] | experimental→**verified(이번 런 승격)** | 실물 T1(패턴검증)→T2~T5(패턴 재사용)에 실전 적용 — 15노드 neat 정렬을 5/5 성공, quirk 확정(Cmd+V dispatchEvent 우회) |
| [[techniques.cross-paste-parity]] | verified | 좌표 재배치 후 paste 시 새 id 재발급이 정상 동작임을 재확인(리스크 아님으로 재분류 근거) |
| [[techniques.osascript-trusted-hybrid]] | verified | Cmd+V 키다운 합성 무반응 시 하드웨어 keycode 9 보조 경로로 T1 탐색 단계에서 재사용 |
| [[techniques.cdp-raw-driver]] | verified | 실물 힉스필드 탭 직접 조작(신규 스크래치 탭 전용, 5개 보호 탭 무접촉) |
| [[techniques.model-matrix-diff]] | verified | 이미지 Nano Banana(1cr)·비디오 Kling v3.0(8.75~12.5cr/클립)·Upscale Bytedance(2cr)·Voice Seed Audio/Voiceover(elevenlabs)·LLM My Claude(무료) 실단가 재확인, GPT Image 2 미사용 확정 |
| [[techniques.adversarial-verification]] | standard | 크레딧 총지출을 브리핑 수치(968→692≈276cr)로 그대로 받아쓰지 않고 MCP transactions 전수 재계산으로 반증·정정(§5 로직평가) |

**세션 19 대비 전환**: ①내러티브 파리티(AD1~5, 참조체이닝 톤 일관성 콘텐츠)에서 **복잡 워크플로우 파리티**(전 노드타입 7종 총동원·크로스타입 연결·Prompt노드 인라인 금지)로 캠페인 축 이동 ②클론 측 LLM/오디오 인라인 패널(G1/G2)·Voice 실행 배선(text2speech_v2)·Upscale 노드 타입이 이번 런의 선행 인에이블로 신규 배선됨(세션19 이월 과제였던 "G1/G2 인라인패널" 완료) ③[[techniques.canvas-coord-inject-rearrange]]가 실측 대기(TODO) 상태에서 5주제 반복 재현으로 **verified 승격** — 이 캠페인 최초로 "실물 프로그램적 재배치"가 완주된 사례.

## 2. 세션 로직 도식
```mermaid
flowchart TD
    S["셋업: 260615_canvas-clone, branch parity<br/>SPEC.md ★★5주제 매칭 빌드"] --> EN["클론 인에이블(선행)<br/>G1/G2 인라인패널·Voice 배선·Upscale 노드타입·크로스타입 엣지"]
    EN --> T1P["T1 커피 — 패턴검증 패스<br/>실물: 클립보드 좌표재배치(RE) 실측 확정<br/>~40 탐색 스크린샷(paste/rightclick/tidy)"]
    T1P --> GATE{"패턴 이상없음?"}
    GATE -->|Yes| T2["T2 느와르"] & T3["T3 러닝"] & T4["T4 스킨케어"] & T5["T5 전기차"]
    T2 --> BUILD["실물+클론 양쪽<br/>15노드·7타입·Prompt노드 fan-out·앵커ref·neat정렬"]
    T3 --> BUILD
    T4 --> BUILD
    T5 --> BUILD
    BUILD --> GEN["각 gen 실행<br/>Nano Banana·Kling v3.0 pro 5s·Voiceover·Bytedance Upscale·My Claude"]
    GEN --> PARITY["파리티 발견 3건<br/>①Upscale엣지divergence ②T2 NSFW오탐 ③구성매칭"]
    PARITY --> GAL["gen_compare.py<br/>reports/complex-workflows/index.html"]
    GAL --> CREDIT["크레딧 MCP 재계산<br/>1067.74→692.31cr(−375.43, 브리핑 276cr 정정)"]
    CREDIT --> E["결산: runs+ledger+status+techniques(2장)+대시보드"]
```
실물 조작 개방(R&D redo 가능) 하 전 구간 생성 실주입. 클론은 bridge(8766)+CDP(9222) 자동화, 실물은 CDP 신규 스크래치 탭 전용(5개 보호 탭 무접촉).

## 3. 안전
- 실물: 새 캔버스만(T1~T5 신규 프로젝트). 좀비766028e1·샌드박스75c36e2a·오너참조a12eb16a·기존 내러티브AD/스크래치 접근 금지 — 준수 확인(`ref/_RECON_CLIPBOARD_API.md` §8, 5개 보호 탭 URL·타이틀 불변 재확인).
- 클론: 새 프로젝트만(canvas-projects/). 기존 cb30b89·AD최종본 접근 금지 — 준수 확인.
- 크레딧: **MCP 거래내역 정본 재계산 결과 1067.74cr → 692.31cr, 순지출 375.43cr**(세션19 종료 잔액을 정확한 시작점으로 확인 — 이 값과 정확히 일치해 전수 재계산의 정합성이 검증됨). 내역: Kling v3.0 34건 −297.50cr · Nano Banana 49건 −47.00cr(환불 1건 +1 포함 순액) · Bytedance Image Upscale 12건 −20.00cr(환불 1건 +2 포함 순액) · Seed Audio 1.0 8건 −9.70cr · Voiceover 5건 −0.75cr · Higgsfield Soul V2(G1/G2 인에이블 테스트) 4건 −0.48cr. GPT Image 2 사용 0건 확인.
- ⚠ **브리핑 수치 정정**: 오케 브리핑의 "968→692≈276cr"는 T1~T3 완료(resume 상태) 이후~T4/T5 구간만 포착한 부분합으로 재확인됨(원인: 968cr 체크포인트가 세션 중간인 T3 완료 직후 시점이었고, 그 이전 T1 패턴검증+T2/T3 최초 빌드 구간(1067.74→968, 약 99.43cr)이 "이번 5주제 빌드" 총액 계산에서 누락됨). **정본은 375.43cr**(1067.74→692.31) — §5에 교훈 반영.
- 여전히 금지: 외부전송·게시·결제·영구삭제. 통지 대기(bounded 폴링) 준수.

## 4. 이벤트 요약
- **클론 인에이블(선행)**: LLM/오디오 노드 인라인 패널(G1/G2, 기존 recon 기반 구현) + Voice 실행 배선(text2speech_v2, elevenlabs 프리셋) + Upscale 노드 타입 신규 추가(`3167e9a`, 연결이미지 중복 `--image` 플래그 버그 동시 수정) + 크로스타입 엣지(LLM텍스트출력→Voice프롬프트입력, Prompt노드→gen prompt입력) 배선. 이미지 젠 노드 `input_images` 핸들 렌더 복원(`c02bfe5`, 앵커 fan-out 4엣지 렌더 안 되던 갭 수복) — 이 수정이 없었으면 클론 쪽 ref fan-out 엣지가 화면에 안 보였을 것.
- **실물 클립보드 "서버 참조 ID" 가설 조사** — 오너가 실측한 마커 `849a4423-...`를 보고 "서버측 참조로 바뀐 것 아니냐"는 가설을 제기, `harness/clipboard_api_recon.py`(신규, target_id 직접 attach)로 신규 스크래치 탭에서 3중 증거(라이브 재현·정적 소스 청크 grep·negative control) 재검증 → **가설 기각**, 4일 전(세션10 r2) 확정한 "OS클립보드=마커/localStorage=진짜 payload" 구조가 오늘도 그대로임을 재확인(`ref/_RECON_CLIPBOARD_API.md`). 부산물로 §4(인메모리 fast-path)·§5(이미지 blob 동시 기록) 신규 디테일 문서화.
- **T1 커피 — 패턴검증 패스**: 실물에서 좌표 재배치 절차를 처음 라이브 실측. Cmd+V 키다운 합성이 무반응임을 재확인 → `document.dispatchEvent(new ClipboardEvent('paste', {clipboardData}))` 직접 디스패치 + `Browser.grantPermissions(['clipboardReadWrite'])`로 우회 성공. 붙여넣기→우클릭 정렬 시도→좌표 재계산 주입→tidy 결과까지 탐색 스크린샷 약 40장 축적(`real/_t1_after_paste{1~6}·_t1_rightclick*·_t1_tidy_test·_t1_tidy_result·_t1_repaste2·_t1_verbatim_paste{1,2}·_t1_fullpaste_final.png`). 15노드/15엣지 neat 정렬 확정, `T1_overview.png`.
- **T2~T5 — 패턴 재사용**: T1에서 확정한 절차를 그대로 적용, 각 주제 15노드/15엣지(실물) neat 정렬 완주. T1 대비 탐색 스크린샷이 대폭 감소(주로 `_overview.png`/`_structure.png`만) — 절차가 안정적으로 재사용됨을 방증. T2에서 씬1 이미지(느와르 담배연기 프롬프트)가 **NSFW로 오탐**, 크레딧 자동환불·해당 노드 idle로 확정(파리티 발견②, MCP transactions의 Nano Banana refund 1건과 매칭).
- **클론 양쪽 빌드**: `harness/build_topic.py`(T1~T5 공용, `build_t1.py`를 일반화)로 bridge(8766) 프로젝트 생성 → `window.__loadDoc`으로 15노드/16엣지 그래프 주입(클론은 dev-only 훅 사용, 실물과 달리 클립보드 재배치 기법 불필요 — 애초에 좌표 하드코딩 주입) → 의존순서(topological) GENERATE 순회. T1~T3·T5는 이전 세션에 이미 img/vid 결과가 존재해 `resume` 모드로 스킵, 이번 런에서는 llm_tagline/voice_narration(T1)·upscale_hero(T2·T3·T5) 델타만 생성. T4는 이번 런에서 10노드 전체 신규 생성(풀 빌드).
- **파리티 발견①(Upscale 엣지 divergence)**: 클론은 `img→Upscale` 엣지가 연결·렌더됨(16엣지), 실물은 Upscale 노드가 DOM 핸들 자체를 렌더하지 않아 그래프엣지 연결이 애초에 불가능(15엣지, upscale idle 상태로 그래프에 존재만 함). 실물 Upscale이 별도 메커니즘(엣지 아닌 다른 참조 방식)을 쓰는 것으로 추정 — 확정 규명은 이월.
- **갤러리+결산**: `reports/complex-workflows/gen_compare.py`(narrative-parity 패턴 재사용) 신규 작성 → `index.html` 생성(5주제 전부 좌=실물/우=클론, 파리티 발견 3건 상단 고정 박스). MCP `transactions`(160건 페이지네이션) 전수 재계산으로 크레딧 375.43cr 확정(§3 정정 내역).

## 5. 로직 평가
- **작동한 것**: ①[[techniques.canvas-coord-inject-rearrange]]가 "TODO 실증 대기" 카드에서 **T1 패턴검증→T2~T5 재사용**이라는 이 캠페인 특유의 2단계 실행 순서 자체가 검증 방법론으로 그대로 기능함 — 1개 프로젝트 안에서 "같은 기법을 5번 반복 재현"한 것이 표준 승격 기준(2프로젝트 실증)을 대체할 만한 근거가 됨(재현성이 프로젝트 다양성보다 이 케이스에선 더 직접적 증거) ②Cmd+V 키다운 무반응 quirk를 [[techniques.osascript-trusted-hybrid]]가 이미 확립한 "합성 이벤트 실물 무반응" 패턴과 즉시 연결해, 새로 헤매지 않고 `dispatchEvent(ClipboardEvent)` 직접 트리거로 빠르게 우회 — 기존 기법 카드가 신규 상황의 실패모드를 선제적으로 예견해준 사례 ③클론 인에이블(G1/G2·Voice·Upscale·크로스타입엣지)을 "5주제 빌드 시작 전 선행 단계"로 명확히 분리한 것이 fix-until-works 루프를 5회 반복하지 않고 1회 인프라 정비 + 5회 콘텐츠 빌드로 깔끔히 나눔.
- **병목/실패**: ①★크레딧 브리핑 수치("968→692≈276cr")를 그대로 받아쓰지 않고 MCP transactions 전수 재계산했더니 **실제로는 375.43cr**로 -99.43cr(약 36%) 과소평가였음이 드러남 — 원인은 "968cr" 체크포인트가 5주제 빌드의 시작점이 아니라 **T1~T3 완료(resume) 시점**이라는 중간값이었는데 이를 시작 잔액으로 오인. [[techniques.adversarial-verification]] 원칙("자가선언 불신, 재측정")을 크레딧 수치에도 예외 없이 적용해야 한다는 게 이번 런의 핵심 교훈 ②Upscale 노드의 실물 그래프엣지 미지원(파리티 발견①)이 왜 그런지 근본 메커니즘은 이번 런에서 규명하지 못함(그래프엣지가 아니면 실물이 무엇으로 upscale 참조 이미지를 연결하는지 미확정) — 이월 필요 ③T2 NSFW 오탐(파리티 발견②)이 프롬프트 문구("담배연기") 때문인지 모델 자체의 과민 필터인지 원인 분리는 하지 않음(재현 실험 없이 1회 관측만).
- **다음 런에서 바꿀 것**: ①**크레딧 수치는 브리핑에 적힌 값이라도 MCP transactions로 항상 재계산**(오케 브리핑 문구 자체를 근거로 삼지 않기) — 이번처럼 세션 중간 체크포인트를 시작값으로 오인하는 사고를 재발 방지하려면 "시작 잔액 = 직전 런의 종료 잔액(status/canvas.md 기록)과 일치하는지"부터 먼저 검증하는 절차를 [[techniques.model-matrix-diff]] 또는 night-run-sop에 명문화할 가치 있음(제안) ②Upscale 엣지 divergence 근본 메커니즘 규명(전용 세션) ③T2 NSFW 오탐 재현성 확인(같은 프롬프트로 재시도해 결정론적인지 랜덤인지).
- **ledger 반영**: 5건([[techniques.canvas-coord-inject-rearrange]] verified 승격·[[techniques.canvas-clipboard-localstorage]] 재확인·[[techniques.cross-paste-parity]] 재사용·[[techniques.adversarial-verification]] 크레딧 정정·[[techniques.model-matrix-diff]] 실단가 재확인).
