---
id: techniques.baseline-then-diff
title: 베이스라인-후-디프 (한 번 전수조사 → 이후 diff-only)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.version-archive-3layer, techniques.webgl-node-rendering-clone, techniques.append-only-logging, techniques.total-fidelity-cloning, techniques.night-run-sop]
evidence:
  - "260615_canvas-clone ref/real-recapture-2026-07-18/_MANIFEST.md (2026-07-18) — 버전 정책: OLD(업그레이드 이전 실물 캡처·recon·상태지도)는 git 태그+기존 ref/ 폴더로 절대 덮어쓰기 금지 보존, UPDATED(현재)는 신규 폴더에만 재캡처 — 매번 처음부터 다시 서베이하지 않고 OLD 대비 드리프트만 추려내는 구조"
  - "260615_canvas-clone ref/real-recapture-2026-07-18/_ARCHIVE-METHOD.md §판단 규율 (2026-07-18) — '기능/구조 변화 → 클론 반영 / 순수 시각 리스타일 → 아카이브만, 픽셀 재스킨 안 쫓음(러닝머신 방지)' 기준을 명문화. 판단 한 줄: '이 변화가 방법론/엔진베이스에 기여하나?'"
  - "260615_canvas-clone ref/real-recapture-2026-07-18/_DECISION-dom-vs-webgl.md (2026-07-18) — '미리 최적화하지 않는다. 병목 나면 그때' — WebGL 재전환을 지금 하지 않고, 구체적 트리거(수백 노드 규모 도달) 발생 시에만 노드 렌더 레이어만 좁게 스왑하기로 결정. 전수 재작업이 아니라 좁은 범위 diff 대응의 사례"
updated: 2026-07-18
owner: 박춘순
---

# 베이스라인-후-디프 (한 번 전수조사 → 이후 diff-only)

**한 줄**: 클론 베이스라인을 만들 땐 **한 번은 전부**(모든 상태·모든 스크린샷) 훑어야 하지만, 그 이후 정상 운영은 **자동 아카이브 + 변경분만 diff**로 전환한다 — 매 업스트림 버전마다 처음부터 다시 서베이/재작도하지 않는다. 러닝머신(원본이 바뀔 때마다 전면 재작업에 쫓기는 상태)을 피하는 관리 원칙.

## 왜 필요한가
클론 대상은 살아있는 앱이라 예고 없이 업그레이드된다([[techniques.webgl-node-rendering-clone]]이 그 실례). 매번 "이번엔 뭐가 바뀌었나"를 전면 재정찰으로 확인하면 캠페인이 원본의 릴리스 속도를 못 따라간다 — 대신 **베이스라인을 한 번 완전히 확보한 뒤, 정상 운영은 훨씬 싼 diff-only 루프**로 돌린다.

## 두 국면
1. **베이스라인 국면**(캠페인 초입, 1회): 클론이 딛고 설 기준선을 위해 전 상태·전 노드타입·전 스크린샷을 모은다. 여기서 아끼면 이후 모든 diff가 "무엇과 비교하는지" 기준이 불안정해진다.
2. **정상 운영 국면**(그 이후, 지속): [[techniques.version-archive-3layer]]로 월 1회 자동 아카이브를 돌리고, **변경이 감지된 부분만** 재조사·재작업한다. 매 세션 처음부터 전체를 다시 훑지 않는다.

## durable vs snapshot — 무엇을 유지하고 무엇을 흘려보내나
| 구분 | 정의 | 예시 | 운영 |
|---|---|---|---|
| **durable(유지)** | 캠페인이 계속 참조·재사용하는 것 | 데이터모델(노드 스키마), 방법론/기법 카드, 하네스 코드, 오너 결정 | 계속 관리·갱신, 이 KB의 techniques/에 축적 |
| **snapshot(흘려보냄)** | 특정 시점에만 유효한 것 | 스크린샷, UI 레이아웃, 모델 목록, 픽셀 룩 | **날짜를 찍고 동결** — 다음 버전이 나와도 쫓아가지 않음, 필요하면 새 스냅샷을 새로 뜬다 |

원칙: **element map(요소지도)은 "그 날짜 시점 클론을 만들기 위한 학습 자료"이지 실물의 라이브 미러가 아니다.** 실물이 리스타일되면 그 element map은 자동으로 낡지만, 그건 결함이 아니라 애초 성격이 그렇다 — 다시 뜨면 될 일.

## 판단 규율 (diff 발생 시 반영 여부)
- **기능/구조 변화**(새 노드타입·새 모델·새 파라미터·새 컨트롤) → **클론에 반영**. DOM/JSON으로 캡처 가능하고 클론의 기능적 파리티에 영향.
- **순수 시각 리스타일**(픽셀 룩만 변화, 기능은 동일) → **아카이브만**, 쫓지 않는다.
- 한 줄 기준: **"이 변화가 방법론/엔진베이스에 기여하나?"** 예 → 반영 / 아니오 → 아카이브.
- 미리 최적화하지 않는다 — 트리거가 실제로 발생하기 전엔 대비만 해두고(예: 데이터/렌더 분리 구조), 전환 작업 자체는 트리거 발생 시점까지 미룬다([[techniques.webgl-node-rendering-clone]] §클론 전략의 "재고 조건" 사례 참고).

## 함정
- **베이스라인 국면을 생략하고 바로 diff-only로 가면 기준선이 없다** — 첫 캡처가 부실하면 이후 모든 "변경분만"이 실은 처음부터 못 봤던 것일 수 있다. 베이스라인은 아끼지 않는다.
- **snapshot을 durable처럼 관리하려는 유혹** — 스크린샷/레이아웃을 매번 최신으로 맞추려 들면 그게 러닝머신이다. snapshot은 날짜 찍고 동결, durable만 계속 갱신.
- **"기여하나?" 판정을 빌더가 혼자 내리지 않는다** — [[techniques.total-fidelity-cloning]]의 "무해 단순화는 오너 확인 전까지 열린 항목" 규율과 같은 이유로, 애매한 diff는 오너 승인 전까지 아카이브 상태로 열어둔다.

## 관련
- [[techniques.version-archive-3layer]] — 이 원칙이 실제로 도는 하부 메커니즘(월 1회 3층 캡처)
- [[techniques.webgl-node-rendering-clone]] — "재고 조건이 오기 전까지는 지금 아키텍처 유지" 결정이 이 원칙의 실례
- [[techniques.total-fidelity-cloning]] — "무해 단순화 자체 판정 금지" 규율과의 접점(둘 다 "판단을 언제 닫는가"를 다룸)
- [[techniques.append-only-logging]] — diff 이력을 append-only로 남기는 것과 결합하면 "언제 무엇이 바뀌었나"가 재구성 가능
