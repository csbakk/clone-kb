---
id: cases.canvas
title: 캠페인 사례 — Higgsfield Canvas 클론 (260615_canvas-clone)
doctype: case
status: verified
proven_in: [canvas]
related: [pipelines.rip-v1, pipelines.99-percent, pipelines.verify-first-loop, techniques.dogfooding-as-bug-discovery, techniques.structure-first-cloning]
evidence:
  - "~/Documents/project/260615_canvas-clone/ (외부 경로, 이 KB는 포인터만 보유)"
updated: 2026-07-17
owner: 박춘순
---

# 캠페인 사례 — Higgsfield Canvas 클론

**외부 작업폴더**: `~/Documents/project/260615_canvas-clone/` (실물 앱: Higgsfield Canvas, 노드캔버스형 생성 AI 툴)

## 현재 상태 (2026-07-17 세션21 기준)
- **dev 서버**: `localhost:5175` (`npm run dev`) · **CDP 포트**: 9222/9223, 프로필 `~/.chrome-canvas-clone` · **RIP 스크래치 캔버스 영구고정**: `3ad36980c5eb`(세션18부터, url_substr 모호성 방지)
- **파리티 게이트**: 9종 통과 (셸·노드·인터랙션·모델/업로드·상태/서피스/도구·크롤러·**크로스-페이스트**) — 99% 판정식 항목④ 달성(2026-07-13 세션 10)
- **RIP 레이어① 상태**: 19/19 전수 덤프, 0 스킵. attribute-diff 38,476 → 30,580(세션7 리셋) → isolated 기준선 33,538 → 28,642(세션11) → 27,762(세션12) → 23,581(세션16 큐 근본수정, 진짜 총계 재확정) → 22,626(세션16 후속) → 17,490(세션17, window-size 노이즈 −3,558 분리) → 17,425(세션19) → **17,113**(세션21, canvas-id 고정+뷰포트정규화 재덤프, 유령2건 종결)
- **테스트**: `npx vitest run` — 102/102(세션21 기준, 프롬프트골격 리팩터 6라운드 전부 무회귀), 상시 GitHub Actions CI
- **브랜치**: `polish-effects`(구 데모 레이어, 2026-07-13 철거) vs `parity`(활성 캠페인 브랜치)
- **방법론 축(세션21)**: [[techniques.structure-first-cloning]] canvas 소급 적용(retrofit) — 스타일-먼저로 누적 진행돼온 이 캠페인에 "골격→스타일→동작" 원칙을 처음 이식. 상세는 `ref/_STRUCTURE_FIRST_ROADMAP.md`.

## 이 캠페인이 낳은 기법
- [[techniques.rip-css-dump]] · [[techniques.rip-crawler]] · [[techniques.rip-repair-loop]] — RIP 3단 파이프라인 원류 ([[pipelines.rip-v1]])
- [[techniques.cdp-raw-driver]] — 좀비 탭 우회 (cdp_raw.py)
- [[techniques.model-matrix-diff]] — 66개 모델 카탈로그 전수 검증, GENERATE 비용 0
- [[techniques.dogfooding-as-bug-discovery]] — BORI 사례, 실사용 4회 실생성으로 6개 실버그 발견·수정
- [[techniques.url-escape-guard]] — 크롤러가 실제로 유발한 네비게이션 사고에서 신설
- [[techniques.orchestrator-model-routing]] — 빌더(sonnet)≠검증자(opus/fable) 규칙의 원 출처
- [[pipelines.99-percent]] — 6축 판정식 정의 원 출처
- [[techniques.cross-paste-parity]] — P1 파일럿(세션 10)으로 verified 승격: 실물 직렬화 계약(마커+localStorage) 채택, 왕복 4/4 diff 0. [[techniques.clipboard-source-of-truth]]의 "클립보드에 JSON 직접" 서술을 교정한 재실측(r2)도 이 라운드의 산물
- [[techniques.canvas-clipboard-localstorage]] — 클립보드 2단 구조(OS마커+localStorage payload) 3중 증거 확정, 세션20에 "서버참조ID" 가설 재검증으로 재확인
- [[techniques.canvas-coord-inject-rearrange]] — 세션20에 실물 T1~T5 5/5 성공으로 experimental→verified 승격, 프로그램적 좌표 재배치 절차 확정
- [[techniques.structure-first-cloning]] — 세션21에 canvas가 이 원칙의 **retrofit 시나리오 첫 실증**(카드 §함정 "이미 스타일-먼저 캠페인은 골격을 소급 교체" 시나리오). 헤더span·라이트박스메타패널·프롬프트골격 6타입 순차 리트로핏, proven_in에 canvas 추가

## 현재 캠페인 루프 (도식 — 결산 시 갱신)

```mermaid
flowchart LR
    subgraph LOOP["운영 루프 (오케=Fable · 빌더=sonnet · 검증=opus)"]
        REC["정찰/립<br/>rip_dump·crawl (실물, 스크립트)"] --> GAP["델타/갭 매트릭스<br/>= 작업 큐"]
        GAP --> BUILD["빌더 서브에이전트<br/>실측값만, 추측 금지"]
        BUILD --> VER["적대 검증자<br/>자가선언 불신·재측정"]
        VER -->|"결함"| BUILD
        VER -->|"통과"| GATE["게이트 선언 + 커밋"]
        GATE --> RETRO["결산: 원장 append<br/>+ 대시보드 재생성"]
        RETRO --> REC
    end
    USER["사용자 실사용 리포트<br/>(영상·도그푸딩)"] -->|"사각 발견"| GAP
    RETRO -.->|"기법 승격/은퇴 Issue"| KB["clone-kb 무기고"]
```

**진행 단계 (99% 로드맵 — [[pipelines.99-percent]])**:
| 단계 | 상태 |
|---|---|
| 게이트 8종 (셸~크롤러) | ✅ 통과 |
| P1 크로스-페이스트 | ⬜ 미착수 (다음) |
| P2 탐사기+델타 소탕 | ⬜ |
| P3 애니메이션 립→쌍둥이 미러 | ⬜ |
| P4 픽셀 지문→99% 판정식 | ⬜ |

## 잔여 티켓 / 남은 일
- RIP 잔여 델타: 잔여 커서 미세매칭 1건(세션21 cursor:text 소급수정 후 남은 아티팩트 추정) — 시스템 토큰으로 안 잡히는 컴포넌트별 케이스워크로 분류.
- 모델피커 플라이아웃·인스펙터 피커 — RIP role 자동판정 불가, 육안대조 전용 세션 필요(세션21 정찰에서 재확인).
- LLM/Audio 노드 전용 RIP state-spec 부재 — IME하네스+tsc+vitest로만 검증 중, 스타일 레벨 회귀는 육안 스팟체크 의존(세션21 이월).
- 핸들/엣지/툴바 RIP 커버리지갭 — 세션21에서 핸들만 리트로핏, 엣지·툴바 미착수.
- `IMETextarea.tsx` 삭제 — 6개 소비처 전부 이탈 확인(세션21), 파일 자체는 미삭제.
- Upscale 엣지 실물 메커니즘 근본 규명 · T2 NSFW 오탐 재현성 확인(세션20 이월).
- 크롤러 상태 커버리지 확장.
- 99% 판정식 P1(cross-paste)~P4(pixel-fingerprint) 전부 미착수 — [[pipelines.99-percent]] 참고.
- 커스터마이징 트랙(Comfy 노드, live LLM planner)은 `src/live/`에 보존만 된 채 미배선.

## 최근 세션
2026-07-17 세션21 — [[techniques.structure-first-cloning]] canvas 최초 소급 레트로핏(핸들·헤더span·라이트박스메타패널·프롬프트골격 6타입 contentEditable화), RIP 재덤프 17,425→17,113, 0크레딧. 상세: `clone-kb runs/2026-07-17-canvas-structfirst.md`.
