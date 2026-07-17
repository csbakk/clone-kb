---
id: techniques.canvas-coord-inject-rearrange
title: 복사→좌표수정→주입 재배치 (프로그램적 격자정렬)
doctype: technique
status: experimental
proven_in: []
related: [techniques.canvas-clipboard-localstorage, techniques.clipboard-source-of-truth, techniques.atomic-localstorage-inject, techniques.cross-paste-parity]
evidence:
  - "TODO — 실물 빌더 라이브 테스트 진행 중(2026-07-17 기준). 결과 미도착 — 이 문서는 방법론만 기록, 실측 확정치(성공/실패·quirk·소요시간)는 다음 갱신에서 반영"
updated: 2026-07-17
owner: 박춘순
---

# 복사→좌표수정→주입 재배치 (프로그램적 격자정렬)

**한 줄**: 캔버스에 흩어진 노드 다수를 하나씩 드래그하는 대신, 전체(또는 부분) 선택→복사→[[techniques.canvas-clipboard-localstorage]]로 노출된 JSON을 읽어 **좌표(x/y) 필드만 프로그램으로 재계산(격자/열 정렬)**한 뒤 되쓰고 → 원본 삭제 후 붙여넣기로 재주입 = 한 번에 깔끔한 재배치.

> ⚠ **실증 대기**: 이 카드는 오너 아이디어를 기법 카드 포맷으로 선구조화한 것 — 실물 빌더의 라이브 테스트 결과가 아직 도착하지 않았다. 아래 절차는 [[techniques.canvas-clipboard-localstorage]]가 실측 확정한 메커니즘 위에 논리적으로 구성한 **예상 절차**이며, quirk(엣지 재연결, id 재매핑, undo 히스토리 등)는 실측 전까지 미확정이다. 결과 도착 시 이 문서를 갱신하고 status를 experimental→verified로 재평가할 것.

## 언제 쓰나
- 노드 캔버스에 노드가 무작위/뒤죽박죽 배치되어 있어 정렬이 필요한데, 노드 수가 많아 수동 드래그가 비효율적일 때(O(n) 드래그 대신 O(1) 스크립트 재배치).
- 앱 자체에 "Tidy up"/자동정렬 기능이 없거나, 있어도 원하는 배치 규칙(특정 격자·열 순서)을 세밀하게 제어하고 싶을 때.

## 사전조건
대상 앱이 [[techniques.canvas-clipboard-localstorage]]가 정의하는 "OS클립보드=마커, 진짜 payload=localStorage(또는 IndexedDB)" 패턴을 쓴다는 게 먼저 실측 확인되어 있어야 한다. 이 전제가 없으면 3단계(좌표 재계산)가 애초에 불가능.

## 절차 (예상 — 실측 전)
1. **선택**: 캔버스에서 재배치할 노드들을 전체선택(Cmd+A) 또는 부분선택.
2. **복사**: Cmd+C → [[techniques.canvas-clipboard-localstorage]] 절차로 `localStorage[key]`의 `{marker, payload}`를 읽는다. `payload`를 파싱하면 `{nodes:[...], edges:[...]}` 형태(canvas 실측 스키마 기준).
3. **좌표 재계산**: `nodes[].position`(또는 앱별 x/y 필드명)을 순회하며 격자/열 정렬 함수로 새 좌표를 계산.
   - 예: 열(column) 개수 N, 카드 폭 W, 행간격 H를 지정해 `x = col * (W + gapX)`, `y = row * (H + gapY)`로 재배치.
   - 원본 상대 순서(생성 순 또는 기존 y좌표 순)를 정렬 키로 쓸지, 노드 타입별 그룹핑을 할지는 케이스별 결정.
4. **되쓰기**: 재계산된 JSON을 `JSON.stringify`해서 **같은 marker로** `localStorage.setItem(key, {marker, payload:newPayload})` — [[techniques.atomic-localstorage-inject]]의 "여러 write 대신 한 번에 합쳐서 한 번의 write" 원칙 적용(레이스 방지). OS 클립보드 마커 문자열은 그대로 두거나(같은 marker 유지 시) 갱신.
5. **원본 삭제**: 선택된 원본 노드들을 캔버스에서 Delete(그대로 두면 붙여넣기 후 중복 노드가 남음).
6. **주입**: Cmd+V → 앱의 paste 핸들러가 localStorage payload를 읽어 재계산된 좌표로 새 노드를 materialize. [[techniques.cross-paste-parity]] 실측(canvas)에 따르면 paste는 **항상 새 id를 재발급**하므로, 재배치 후 노드 id가 원본과 달라지는 것은 정상 동작으로 예상됨(원본 id에 의존하는 다른 참조가 있다면 별도 확인 필요).

## 대안
앱에 자체 "Tidy up"/자동정렬 기능이 있으면 그것부터 시도 — 이 기법은 그 기능이 없거나 세밀 제어가 필요할 때의 대체 경로.

## 리스크·미확정 사항 (실측 전 — TODO)
- **엣지 재연결**: 좌표만 바꾸고 노드 간 연결(edges)이 좌표 변경 후에도 정상 유지되는지 미확인. [[techniques.clipboard-source-of-truth]] §함정이 "붙여넣기로 엣지가 유실되는 경우가 있었다"를 이미 경고 — 이 기법에서도 같은 리스크 상속 가능성.
- **id 재매핑과 외부 참조**: paste가 새 id를 발급하면(§절차 6), 캔버스 밖에서 그 노드 id를 참조하는 것(예: 히스토리, 딥링크)이 있을 경우 깨질 수 있음.
- **대량 노드 시 성능**: 노드 수가 매우 많을 때 좌표 diff가 크면 렌더/애니메이션 부하가 어떤지 미확인.
- **undo 히스토리**: 원본 삭제+주입이 앱의 undo 스택에서 어떻게 기록되는지(한 번의 undo로 되돌아가는지, 여러 단계로 쪼개지는지) 미확인.
- **소요시간·안정성**: 실측 성공률·실패 모드 미기록.

## 실증
TODO — 실물 빌더 라이브 테스트 결과 도착 시 이 섹션에 반영(성공/실패, 발견된 quirk, 최종 확정 절차로 §절차 갱신).

## 크로스툴 가설
[[techniques.canvas-clipboard-localstorage]]의 크로스툴 가설이 어떤 도구에서 실측 확인되면(즉 그 도구도 "OS클립보드=마커, payload=로컬" 패턴을 쓰면), 이 좌표 재계산+재주입 기법도 그 도구로 이식 가능할 것으로 예상 — 좌표 필드 재계산 로직 자체는 Higgsfield 종속이 아니라 일반적인 JSON 조작이기 때문. 단, 이식 시 그 도구의 실제 노드 스키마(좌표 필드명, 좌표계 원점, 단위)를 재실측해야 한다.

## 관련
- [[techniques.canvas-clipboard-localstorage]] — 이 기법이 의존하는 클립보드 메커니즘(전제조건)
- [[techniques.atomic-localstorage-inject]] — 되쓰기 시 원자적 write 원칙(레이스 방지)
- [[techniques.cross-paste-parity]] — paste 의미론(id 재매핑 등) 실측 근거
- [[techniques.clipboard-source-of-truth]] — 상위 원칙 및 엣지 유실 함정 선례
