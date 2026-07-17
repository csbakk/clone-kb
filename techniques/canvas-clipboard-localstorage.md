---
id: techniques.canvas-clipboard-localstorage
title: 캔버스 클립보드 = OS마커 + localStorage JSON 패턴 (크로스툴 가설)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.clipboard-source-of-truth, techniques.cross-paste-parity, techniques.atomic-localstorage-inject]
evidence:
  - "260615_canvas-clone ref/_RECON_CLIPBOARD_API.md (2026-07-17) — 실물 재현+정적 소스분석(JS청크 grep)+음성대조 3중 증거. Cmd+C 시 OS클립보드=마커(`higgsfield-canvas-clipboard:<uuid>`)만, 실제 {nodes,edges} JSON은 localStorage['higgsfield-canvas-clipboard']={marker,payload}. Cmd+C~V 전 구간 네트워크 요청 0건(Network.enable 캡처), 해당 138KB 청크에 fetch(/api/ 리터럴 0건"
  - "260615_canvas-clone ref/_RECON_clipboard_r2.md (2026-07-13, '세션10') — 동일 2단 구조를 먼저 특정한 원 정찰. 4일 후 재검증(위 문서)에서도 변경 없음"
updated: 2026-07-17
owner: 박춘순
---

# 캔버스 클립보드 = OS마커 + localStorage JSON 패턴 (크로스툴 가설)

**한 줄**: Higgsfield Canvas는 Cmd+C 때 OS 클립보드엔 짧은 마커 문자열만 쓰고, 실제 그래프 페이로드(JSON)는 `localStorage`에 별도로 저장한다 — **서버 왕복 없음**. 이 "OS클립보드=경량 포인터 / 진짜 payload=탭 로컬 스토리지" 설계는 다른 캔버스·노드형 웹앱(Notion, Miro, Figma, FigJam 등)도 채택했을 수 있다는 게 이 카드의 **크로스툴 가설**(미검증, 도구별 실측 필요).

> 이 카드는 [[techniques.clipboard-source-of-truth]](일반 원칙: 노드캔버스 앱의 정본은 Cmd+C 직렬화)의 **구체 메커니즘 실측 기록 + 크로스툴 재사용 확장**이다. Higgsfield Canvas 자체에 대해서는 verified(3중 증거로 확정), 다른 도구로의 일반화는 experimental.

## 언제 쓰나
- 새 캔버스/노드형 웹앱을 클론·추출할 때, "복사한 데이터가 대체 어디 있나"를 찾는 첫 단계.
- Cmd+C 직후 `pbpaste`로 본 OS 클립보드 내용이 이상하게 짧거나 UUID/토큰처럼 보일 때 — **"서버에 있나보다"로 넘겨짚지 말고 먼저 로컬(localStorage/IndexedDB)부터 덤프해볼 것.** (Higgsfield에서 실제로 이 오판이 발생했었음 — §함정 참고)

## 메커니즘 (Higgsfield Canvas 실측, 2026-07-17 재확정)
1. Cmd+C 핸들러가 선택된 노드/엣지를 `JSON.stringify({nodes, edges, ...})`로 직렬화(`p`).
2. 새 마커 `higgsfield-canvas-clipboard:<crypto.randomUUID()>`(`v`)를 생성.
3. `localStorage.setItem('higgsfield-canvas-clipboard', JSON.stringify({marker:v, payload:p}))` — **여기가 진짜 데이터.**
4. OS 클립보드(`navigator.clipboard`/`document.execCommand`)에는 마커 문자열 `v`만 기록.
5. Cmd+V 시: OS 클립보드에서 마커를 읽고 → `localStorage.getItem(key)` → `marker` 일치 검증 → `payload` 파싱 → materialize. **불일치/누락 시 그래프 붙여넣기는 100% 실패**하고 전혀 다른 폴백 경로(일반 이미지 업로드)로 샌다 — 서버 fallback 없음(negative control로 실증, §7 원문 §6).
6. 같은 탭 세션 안에서는 인메모리 클로저 캐시(`O.current`)가 있어 localStorage조차 다시 안 읽는 fast-path도 존재(리로드하면 사라짐, 영속 계층은 어디까지나 localStorage).

**추출법**: 콘솔에서 `copy(localStorage.getItem('higgsfield-canvas-clipboard'))` 또는 CDP `Runtime.evaluate`로 동일 키 read.

## ★크로스툴 가설 (오너 관심 — 미검증)
Notion·Miro·Figma·FigJam 같은 다른 캔버스/블록/노드 도구도 구조적으로 같은 이유(대량 JSON을 OS 클립보드에 직접 넣으면 무겁고, 외부 앱 붙여넣기 호환성 문제·타 앱 스크래핑 노출도 있음)로 "OS클립보드=경량 마커, 진짜 payload=탭 로컬(localStorage 또는 IndexedDB)" 패턴을 쓸 가능성이 있다. **도구마다 실측 전에는 가설일 뿐** — 아래 절차로 도구별 확인.

### 검증 절차 (도구 불문 공통, canvas에서 쓴 3중 증거 방법론 재사용)
1. **복사→덤프**: 대상 앱에서 뭔가 복사(Cmd+C) 직후
   - OS 클립보드 확인: `pbpaste` (텍스트) — 마커처럼 짧고 UUID/토큰 형태인지 확인.
   - `localStorage` 전체 키 덤프: 콘솔 `Object.keys(localStorage)` → 앱 이름이 들어간 키 후보 탐색(예: `<앱이름>-clipboard`, `<앱이름>_clipboard`, `clipboard:<workspace-id>` 등).
   - `IndexedDB`도 확인(Notion류는 IndexedDB를 더 많이 씀 — `indexedDB.databases()`로 DB 목록, 각 DB의 object store 순회).
2. **음성대조(negative control)**: 마커는 유지한 채 localStorage/IndexedDB의 후보 페이로드만 강제 삭제 후 Cmd+V 시도 → 붙여넣기가 실패하거나 다른 폴백(예: 순수 텍스트/이미지 붙여넣기)으로 새면 "그 로컬 저장소가 진짜 payload였다"는 확정 증거. (canvas에서 이 방법으로 서버 fallback 없음을 실증 — 재사용 가치 높은 절차.)
3. **정적 소스 grep** (가능하면): 배포된 JS 번들에서 `clipboard` 키워드로 관련 청크를 특정 → `localStorage`/`indexedDB` 호출부와 `fetch(`/`/api/` 유무를 대조. `fetch(` 0건이면 서버 왕복 없는 순수 로컬 패턴 확정.
4. **네트워크 캡처**: 복사~붙여넣기 전 구간 Network 도메인 활성화 후 요청 0건 확인(있으면 그건 클립보드가 아니라 별도 사이드이펙트일 가능성 — 구분 필요).

### 확인 대상 도구·키 후보 (미검증, 조사 시작점)
| 도구 | 확인할 저장소 | 키 이름 추정(실측 필요) |
|---|---|---|
| Notion | IndexedDB(주로 씀 — [[techniques.atomic-localstorage-inject]] notion 사례가 localStorage도 병행 확인) | `notion-clone` 류 워크스페이스 키, block clipboard 관련 키 |
| Miro | localStorage/IndexedDB | 보드/위젯 clipboard 키 (미조사) |
| Figma/FigJam | 대부분 WASM+커스텀 바이너리 클립보드 포맷(`fig-kiwi` 등) 사용 이력 보고됨 — **이 패턴과 다를 가능성 높음**, 별도 실측 우선 필요 |

## 함정
- **OS 클립보드만 보고 "서버 참조인가보다"로 오판하기 쉽다** — Higgsfield에서 오너가 짧은 마커 문자열만 보고 이렇게 추정했다가, 실제로는 4일 전부터 동일했던 로컬 2단 구조였음이 재확인됨(§원문 §7). 크로스툴 조사에서도 같은 오판을 피하려면 **로컬 스토리지부터 먼저 덤프**.
- 앱·버전마다 반드시 재실측 — 이 문서는 "패턴이 존재할 수 있다"는 가설과 "확인하는 방법"을 제공하는 것이지, 특정 타 도구가 이 패턴을 쓴다고 확정하지 않는다.
- 인메모리 fast-path(§메커니즘 6) 때문에 "리로드 직후에도 즉시 붙여넣기 가능"처럼 보이는 현상은 로컬스토리지 검증만으로는 설명 안 될 수 있음 — 같은 탭 세션 여부를 구분해서 테스트.

## 관련
- [[techniques.clipboard-source-of-truth]] — 상위 일반 원칙(정본=Cmd+C 직렬화)
- [[techniques.cross-paste-parity]] — 이 메커니즘을 라운드트립 diff 0 게이트로 구현·확장한 후속 기법
- [[techniques.atomic-localstorage-inject]] — localStorage에 되쓸 때 원자적 write 원칙(이 패턴 위에서 좌표 재배치 등 응용 시 필수, → [[techniques.canvas-coord-inject-rearrange]])
