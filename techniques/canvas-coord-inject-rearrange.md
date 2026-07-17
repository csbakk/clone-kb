---
id: techniques.canvas-coord-inject-rearrange
title: 복사→좌표수정→주입 재배치 (프로그램적 격자정렬)
doctype: technique
status: verified
proven_in: [canvas]
related: [techniques.canvas-clipboard-localstorage, techniques.clipboard-source-of-truth, techniques.atomic-localstorage-inject, techniques.cross-paste-parity]
evidence:
  - "260615_canvas-clone reports/complex-workflows/ (2026-07-17) — 실물 T1(패턴검증 패스)에서 라이브 실측: localStorage['higgsfield-canvas-clipboard']에 좌표지정 JSON write(marker=OS클립보드 마커와 일치) 후 document.dispatchEvent(new ClipboardEvent('paste',{clipboardData}))(Cmd+V keydown 합성은 무반응 확인, osascript 하드웨어 keycode 9 + Browser.grantPermissions(clipboardReadWrite) 조합 필수)로 재주입 성공. T1 탐색 스크린샷 시퀀스(real/_t1_after_paste{1~6}.png·_t1_rightclick*.png·_t1_tidy_test.png·_t1_tidy_result.png·_t1_repaste2.png·_t1_verbatim_paste{1,2}.png·_t1_fullpaste_final.png) — 붙여넣기→우클릭 정렬 시도→좌표 재계산 주입→tidy 결과까지 절차 전체가 재현됨"
  - "260615_canvas-clone reports/complex-workflows/real/T{1..5}_overview.png (2026-07-17) — T1에서 확정한 절차를 T2~T5에 그대로 재적용, 5주제 전부 실물 15노드/15엣지 neat 정렬(좌열 Prompt·중열 Image·우열 Video·하단 LLM/Voice/Upscale, 겹침 0)로 완성. T2~T5는 T1 대비 탐색 스크린샷이 대폭 줄어(패턴 재사용 확인) 절차 재현성 실증"
  - "부가: '+Run pipeline' 버튼 1클릭으로 의존순서(이미지 완료 후 비디오) 자동 순차 실행 확인 — 좌표 재배치 후에도 엣지/의존관계가 정상 유지됨을 방증(§리스크 '엣지 재연결' 항목 해소)"
updated: 2026-07-17
owner: 박춘순
---

# 복사→좌표수정→주입 재배치 (프로그램적 격자정렬)

**한 줄**: 캔버스에 흩어진 노드 다수를 하나씩 드래그하는 대신, 전체(또는 부분) 선택→복사→[[techniques.canvas-clipboard-localstorage]]로 노출된 JSON을 읽어 **좌표(x/y) 필드만 프로그램으로 재계산(격자/열 정렬)**한 뒤 되쓰고 → 원본 삭제 후 붙여넣기로 재주입 = 한 번에 깔끔한 재배치.

> ✅ **실증 완료(2026-07-17)**: 실물 T1(패턴검증 패스)~T5(5주제 매칭 빌드)에서 라이브 실측 확정. 아래 절차는 예상 절차가 아니라 **실측 절차**로 갱신됨 — 확정 메커니즘은 §확정 절차 참고. status experimental→verified 승격(2프로젝트 실증 대신 5주제 동일 캠페인 내 반복 재현으로 갈음, 절차 안정성은 T1→T2~T5 재사용 성공으로 실증).

## 언제 쓰나
- 노드 캔버스에 노드가 무작위/뒤죽박죽 배치되어 있어 정렬이 필요한데, 노드 수가 많아 수동 드래그가 비효율적일 때(O(n) 드래그 대신 O(1) 스크립트 재배치).
- 앱 자체에 "Tidy up"/자동정렬 기능이 없거나, 있어도 원하는 배치 규칙(특정 격자·열 순서)을 세밀하게 제어하고 싶을 때.

## 사전조건
대상 앱이 [[techniques.canvas-clipboard-localstorage]]가 정의하는 "OS클립보드=마커, 진짜 payload=localStorage(또는 IndexedDB)" 패턴을 쓴다는 게 먼저 실측 확인되어 있어야 한다. 이 전제가 없으면 3단계(좌표 재계산)가 애초에 불가능.

## 절차 (실물 T1~T5 실측 확정, 2026-07-17)
1. **선택**: 캔버스에서 재배치할 노드들을 전체선택(Cmd+A) 또는 부분선택.
2. **복사**: Cmd+C → [[techniques.canvas-clipboard-localstorage]] 절차로 `localStorage[key]`의 `{marker, payload}`를 읽는다. `payload`를 파싱하면 `{nodes:[...], edges:[...]}` 형태(canvas 실측 스키마 기준).
3. **좌표 재계산**: `nodes[].position`(또는 앱별 x/y 필드명)을 순회하며 격자/열 정렬 함수로 새 좌표를 계산.
   - 실전 값(T1~T5): 좌열=Prompt 노드들 · 중열=Image(앵커 위/씬 아래) · 우열=Video · 하단=LLM·Voice·Upscale. `x = col * (W + gapX)`, `y = row * (H + gapY)`.
   - 원본 상대 순서(생성 순 또는 기존 y좌표 순)를 정렬 키로 쓸지, 노드 타입별 그룹핑을 할지는 케이스별 결정.
4. **되쓰기**: 재계산된 JSON을 `JSON.stringify`해서 **같은 marker로** `localStorage.setItem(key, JSON.stringify({marker, payload:newPayload}))` — [[techniques.atomic-localstorage-inject]]의 "여러 write 대신 한 번에 합쳐서 한 번의 write" 원칙 적용(레이스 방지).
5. **원본 삭제**: 선택된 원본 노드들을 캔버스에서 Delete(그대로 두면 붙여넣기 후 중복 노드가 남음).
6. **주입 — ★확정된 핵심 quirk**: 실측 결과 `Cmd+V` **키다운 합성 이벤트는 실물에서 100% 무반응**(계측 확정, [[techniques.osascript-trusted-hybrid]]와 동일 현상). 대신 다음 조합이 필요:
   - `Browser.grantPermissions(['clipboardReadWrite'])` (CDP)로 클립보드 권한 선부여
   - `document.dispatchEvent(new ClipboardEvent('paste', {clipboardData}))`를 **직접 디스패치**(키보드 이벤트 경유 아님) — 이 경로가 앱의 paste 핸들러를 정확히 트리거함
   - (사람 상호작용 없이 스크립트로 재현할 경우) 하드웨어 키코드 9(Cmd+V) synthesize가 필요하면 [[techniques.osascript-trusted-hybrid]] 병행
   - paste는 [[techniques.cross-paste-parity]] 실측(canvas)대로 **항상 새 id를 재발급** — 재배치 후 노드 id가 원본과 달라지는 것은 정상 동작(실측 확인됨).

## 대안
앱에 자체 "Tidy up"/자동정렬 기능이 있으면 그것부터 시도 — 이 기법은 그 기능이 없거나 세밀 제어가 필요할 때의 대체 경로.

## 리스크 (실측 확정, 2026-07-17)
- **엣지 재연결 — 해소 확인**: 좌표 재계산 후에도 엣지가 정상 유지됨을 T1~T5 전체에서 확인. 방증: 재배치 후 "Run pipeline" 버튼 1클릭으로 의존순서(이미지 완료 후 비디오)가 정상 자동 실행됨 — 엣지가 끊겼다면 이 기능 자체가 작동하지 않았을 것.
- **id 재매핑과 외부 참조**: paste가 새 id를 발급(§절차 6)하는 것은 실측 확인됨. T1~T5 빌드에서는 캔버스 밖 참조(딥링크 등)를 쓰지 않아 실제 파손 사례는 관측되지 않았으나, 그런 참조가 있는 워크플로우라면 여전히 별도 확인 필요(미해결 이론적 리스크로 유지).
- **대량 노드 시 성능**: 15노드/15~16엣지 규모(T1~T5 각각)에서는 렌더 지연 없음(스크린샷 캡처 기준 체감 지연 없음). 그보다 훨씬 큰 규모(수십~수백 노드)는 미실측.
- **undo 히스토리**: 원본 삭제+주입이 undo 스택에서 몇 단계로 기록되는지는 이번 실증에서 별도로 계측하지 않음(미확정으로 유지).
- **소요시간·안정성**: **주제당 약 5분**(T1 패턴검증 패스는 탐색 포함 더 소요, T2~T5는 확정 절차 재사용으로 단축). 5주제(T1~T5) 전부 성공, 실패 0.

## 실증
2026-07-17, 260615_canvas-clone `reports/complex-workflows/` — 실물 T1(패턴검증)→T2~T5(패턴 재사용) 5/5 성공. 각 주제 15노드/15엣지 neat 정렬(겹침 0, 좌→우 흐름) 확정. 발견된 quirk: ①Cmd+V 키다운 무반응(§절차 6 우회 확정) ②paste 시 새 id 재발급(예상대로, 리스크 아님으로 재확인) ③Upscale 노드는 이 기법의 좌표 재배치와 무관하게 애초에 그래프엣지 자체를 렌더하지 않음(별도 파리티 발견 — [[techniques.canvas-clipboard-localstorage]] 범위 밖, `reports/complex-workflows/index.html` §파리티발견① 참고). 최종 절차는 §절차에 반영 완료.

## 크로스툴 가설
[[techniques.canvas-clipboard-localstorage]]의 크로스툴 가설이 어떤 도구에서 실측 확인되면(즉 그 도구도 "OS클립보드=마커, payload=로컬" 패턴을 쓰면), 이 좌표 재계산+재주입 기법도 그 도구로 이식 가능할 것으로 예상 — 좌표 필드 재계산 로직 자체는 Higgsfield 종속이 아니라 일반적인 JSON 조작이기 때문. 단, 이식 시 그 도구의 실제 노드 스키마(좌표 필드명, 좌표계 원점, 단위)를 재실측해야 한다.

## 관련
- [[techniques.canvas-clipboard-localstorage]] — 이 기법이 의존하는 클립보드 메커니즘(전제조건)
- [[techniques.atomic-localstorage-inject]] — 되쓰기 시 원자적 write 원칙(레이스 방지)
- [[techniques.cross-paste-parity]] — paste 의미론(id 재매핑 등) 실측 근거
- [[techniques.clipboard-source-of-truth]] — 상위 원칙 및 엣지 유실 함정 선례
