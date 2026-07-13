# PROTOCOL — 클론 프로젝트에 clone-kb 시스템 주입하기 (에이전트용 규약)

> 어떤 클론 프로젝트든 이 문서 하나로 무기고 시스템에 접속한다. **정본은 이 파일 — 프로젝트에는 포인터만 복사.**

## 0. 이 시스템이 뭔가
- **무기고**: `techniques/`(기법 카드 30+, status: experimental→verified→standard→retired) · `pipelines/`(조립도) · `ledger/`(평가 원장) · `cases/`(캠페인별 진행+루프 도식) · `status/`(무인 런 라이브 상태판 — 덮어쓰기·휘발) · `runs/`(**세션별 런 매니페스트 — append-only 축적.** 로딩 기법+세션 로직 도식+로직 평가. 런끼리 diff=하네스 진화 기록)
- 원칙: 대시보드=파생물(직접 편집 금지, `scripts/gen_dashboard.py`) · 승격/은퇴=Issue 제안→오너 승인 · standard만 skills/ 보유(강등 시 스킬도 제거)

## 1. 주입 절차 (프로젝트당 1회)
1. 이 리포를 로컬 클론(없으면): `git clone https://github.com/csbakk/clone-kb.git ~/Documents/project/clone-kb`
2. 대상 프로젝트의 진입 문서(HANDOFF.md 또는 CLAUDE.md) 상단에 아래 블록 삽입:
   ```markdown
   ## 무기고 (세션 시작 시 먼저)
   **기법 레지스트리 = https://github.com/csbakk/clone-kb** (로컬 ~/Documents/project/clone-kb)
   — 캠페인 시작 전 `index.md`에서 관련 기법 카드만 로드(스킬 로딩 패턴). 운영 의식은 `PROTOCOL.md` §2.
   ```
3. `cases/<프로젝트>.md` 생성(스키마는 기존 케이스 참조): 외부 폴더 경로·현재 상태·루프 도식(mermaid)·잔여 큐
4. `status/<프로젝트>.md` 생성(status/canvas.md 형식 복사): 무인 런 라이브 상태판
5. README 재생성(`python3 scripts/gen_dashboard.py`) 후 push (`gh auth switch --user csbakk` → push → `gh auth switch`)

## 2. 운영 의식 (매 세션 — 오케스트레이터 의무)
| 시점 | 할 일 |
|---|---|
| **캠페인 시작** | clone-kb `index.md` → 이번 작업 관련 카드만 로드 + **`runs/<날짜>-<캠페인>-<주제>.md` 런 매니페스트 생성**(로딩 기법+선택 근거 표·세션 로직 mermaid 도식·안전경계) — "이번 세션은 이 로직으로 돈다"를 시작 시점에 고정 |
| **무인 런 중** | 이벤트(에이전트 투입/완료·게이트·티켓)마다 `status/<프로젝트>.md` 갱신+push — 헤더 🔴 가동/⚪ 대기, 페이즈 mermaid·가동 에이전트 표·티켓 보드·이벤트 타임라인 |
| **세션 결산** | ①`ledger/`에 사용 기법 판정 append(성과/실패/중립+증거 링크) ②**런 매니페스트 §4 로직 평가 채움**(작동한 것/병목/다음 런에서 바꿀 것 — 세션 '로직 자체'의 평가, ledger·승격의 근거) + status:running→done ③`cases/<프로젝트>.md` 진행·도식 갱신 ④`gen_dashboard.py` 재생성 ⑤push |
| **새 기법 탄생** | experimental 카드 등록 → 2프로젝트 실증 시 verified → **Issue로 standard 승격 제안**(오너 승인) |
| **기법이 배신** | 반례를 ledger에 기록, 반복되면 강등/은퇴 Issue (retired는 `superseded_by` 필수) |

## 3. 안전
- 이 리포는 **PUBLIC** — 회사·타사 정보, 실물 앱 자산(SVG·스크린샷·덤프), 토큰 절대 금지. 전부 포인터/경로만.
- 프로젝트 실자산(립 덤프 등)은 각 프로젝트 repo(private)에.
