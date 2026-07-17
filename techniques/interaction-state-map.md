---
id: techniques.interaction-state-map
title: 인터랙션 상태 지도 (노드/컴포넌트 전 버튼→상태 말단까지)
doctype: technique
status: experimental
proven_in: [canvas]
related: [techniques.state-explorer, techniques.state-spec-json, techniques.rip-crawler, techniques.visual-triage-sheet, techniques.clone-documentation-formats, techniques.cdp-nondestructive-recon]
evidence:
  - "260615_canvas-clone/reports/interaction-maps/image-gen-node.html + gen_map.py — 이미지 Generate 노드 파일럿, 상태 21개(S00~S19, 하위 S05/S10b 포함), 0크레딧(GENERATE 미클릭), 신규 라이브 CDP 조작 없이 전부 REC-B/E/F/G/H(2026-07-11~15) 기존 실측 read-only 스크린샷 재사용으로 조립"
  - "260615_canvas-clone/ref/_RECON_HOVER_STATES.md §0 — 'Expand view' 클릭 직후 공유 실시간 캔버스의 결과 노드 1개가 소실된 인시던트(원인 미확정) 기록, 이 기법 카드의 §안전 섹션 근거"
  - "260615_canvas-clone/ref/_RECON_STATES_SURFACES.md §1 — 후속 세션이 디스포저블 샌드박스로 동일 액션(Expand view) 3회 재시도해 인시던트 미재현 확인 → 라이트박스 상태를 안전하게 재확보"
updated: 2026-07-17
owner: 박춘순
---

# 인터랙션 상태 지도 (노드/컴포넌트 전 버튼→상태 말단까지)

**한 줄**: 노드/컴포넌트의 **모든 버튼·컨트롤을 눌러 각각이 여는 상태를 말단 자식까지** 추적해, ①상태 전이 다이어그램 ②컴포넌트 상태 매트릭스 ③스크린샷 갤러리 3개를 한 문서로 합친 복합 포맷. 업계의 wireflow + component state matrix 개념을 클론 정찰에 맞게 결합한 것.

## 상태: 파일럿 완료 (canvas, 이미지 Generate 노드 1종)

[[techniques.state-explorer]]가 "아직 못 본 상태를 도구가 자동 발견"하는 상위 개념(도구 미완성, 커버리지 % 미산출)이라면, 이 기법은 그보다 좁고 구체적이다 — **이미 존재를 아는 노드 타입 하나를 골라, 그 노드의 전 상호작용 표면(버튼·칩·드롭다운)을 사람이 계획적으로 훑어 말단까지 문서화**한다. [[techniques.rip-crawler]](전수 DOM 크롤)나 [[techniques.state-spec-json]](URL+도달절차 재현)과 원자재를 공유하지만, 산출물 형태가 다르다 — 이 기법은 **사람이 한 문서에서 위(전이 그림)→아래(구체 매트릭스)→갤러리(실제 화면)로 드릴다운하며 읽는 것**을 목표로 한다.

## 왜 필요한가

정찰 세션이 쌓이면 "이 버튼 누르면 뭐가 열리더라"가 여러 `_RECON_*.md` 문서에 흩어진다. 인터랙션 상태 지도는 그 흩어진 사실들을 **한 노드 타입 기준으로 재조립**해 다음 두 독자에게 동시에 봉사한다:
- **빌더**: 구현 체크리스트("이 상태들을 다 만들었나") + 각 상태의 DOM 시그니처(children 컬럼).
- **오너/신규 합류자**: 갤러리를 스크롤하며 "이 앱이 뭘 할 수 있나"를 화면으로 파악.

## 만드는 법 (canvas 파일럿 기준)

1. **원자재 재사용을 먼저 확인** — 새로 클릭하기 전에 기존 `_RECON_*.md`·`ref/f_recon/`·`ref/hover/`·`reports/gap-tests/`를 먼저 훑는다. canvas 파일럿은 21개 상태 전부를 **기존 REC-B/E/F/G/H(2026-07-11~15) 세션의 read-only 스크린샷 재사용**만으로 채웠다 — 신규 CDP 조작 0건. 몇 세션에 걸쳐 이미 정찰된 성숙한 캠페인일수록 이 재사용 비율이 높다.
2. **STATES 리스트 하나로 3개 산출물을 자동 생성** — 각 상태를 `{id, category, name, trigger, parent, screenshot, children, notes, source}` dict로 정의하면: mermaid 상태전이 다이어그램(parent→id 엣지를 코드로 순회해 자동 구성) + 표(매트릭스) + 갤러리 카드가 **전부 이 리스트 하나에서 파생**된다. 손으로 다이어그램·표·갤러리를 각각 따로 그리지 않는다(§clone-documentation-formats §AI 소비용 규율과 동일 원칙).
3. **카테고리로 그룹핑** — "노드 생애주기"(idle/hover/selected) → "인스펙터/피커"(Model/Aspect/Resolution/Quality) → "카드 하단 컨트롤"(배치·참조이미지·GENERATE) → "결과 노드(read-only)"(완료 후 hover/캐러셀/라이트박스/컨텍스트메뉴) → "확장 서피스"(빈 노드 우클릭·멀티선택) — 노드 하나가 가진 "생애 단계"를 축으로 삼으면 자연히 말단까지 빠짐없이 훑게 된다.
4. **생성기 스크립트를 재사용 가능하게** — `gen_map.py`는 노드 타입에 종속되지 않는다. 다음 노드 타입(Video Generation·LLM Assistant 등) 파일럿은 STATES 리스트만 교체하면 된다.

## 안전 — "결과 상태는 read-only 관측" 원칙과 인시던트 교훈

REC-B 세션(2026-07-11)에서 완료 결과 노드의 **"Expand view"(라이트박스 열기) 버튼을 클릭한 직후 공유 실시간 캔버스의 결과 노드 1개가 원인 불명으로 사라진 인시던트**가 있었다(§ref/_RECON_HOVER_STATES.md §0). 이후 그 버튼은 재클릭 금지 상태로 남았다가, 후속 REC-F 세션이 **디스포저블(희생 가능) 샌드박스 노드로 3회 재시도**해 인시던트가 재현되지 않음을 확인하고 라이트박스 상태를 안전하게 재확보했다(§ref/_RECON_STATES_SURFACES.md §1).

**교훈**: "결과 상태는 read-only 관측"이 "절대 클릭 금지"를 뜻하지 않는다 — 다만 (a) 실시간 동기화되는 공유 문서가 아니라 **디스포저블 샌드박스**에서, (b) 클릭 직후 즉시 노드 수 카운트+스크린샷 비교로 이상 유무를 확인하며, (c) 과거 인시던트가 있던 액션은 재시도 전 그 기록부터 읽는다. 이 파일럿(2026-07-17)은 한 단계 더 나아가 **재클릭 자체를 생략**하고 이미 안전 확인된 기존 캡처를 재사용했다 — 성숙한 캠페인에서는 "또 클릭해서 재확인"보다 "이미 검증된 기존 증거를 인용"이 더 안전하고 빠르다.

## 관련
- [[techniques.state-explorer]] — 상위 개념(도구가 상태 자체를 자동 발견, 이 기법은 알려진 노드 타입 하나를 계획적으로 훑는 하위 실행)
- [[techniques.rip-crawler]] / [[techniques.state-spec-json]] — 원자재를 공유하는 전수 크롤·재현 스펙 기법
- [[techniques.visual-triage-sheet]] — 스샷+bbox 오버레이 조합이 사람 판독에 강하다는 선행 근거(같은 "스샷+표" 원칙)
- [[techniques.clone-documentation-formats]] — 이 기법이 속하는 상위 "문서화/시각화 포맷 카탈로그"의 한 항목, AI 소비용 포맷 규율은 그 카드 참조
- [[techniques.cdp-nondestructive-recon]] — read-only 관측 원칙의 상위 도그마(3단 체크: 기술/정책/최신 오너지시)
