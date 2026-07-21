---
id: techniques.differential-conformance-pipeline
title: 차등 대조 파이프라인 (1단 규칙표 재생 러너 → 2단 조합 퍼저, 실물을 오라클로)
doctype: technique
status: experimental
proven_in: [notion]
related: [techniques.regression-harness-suite, techniques.adversarial-verification, techniques.state-spec-json, techniques.gate-oracle-staleness]
evidence:
  - "260622_notion-clone/harness/spec_lib.py·spec_runner.py — W-IB(2026-07-21) 신설, W-GQ의 클론전용 러너를 real/both 대조+vacuous-pass 가드로 확장"
  - "260622_notion-clone/harness/spec_fuzz.py — W-ID(2026-07-21) 신설, 998a617에서 백스페이스 2회 버그(FZ004~006)를 손-작성 시나리오가 못 찾던 것을 자동 발견"
  - "260622_notion-clone/behavior-matrix.json — 커버리지 28.1%(64/228, W-GS 인벤토리)→92.7%(215/232, spec_coverage.py 실측)"
  - "260622_notion-clone/_TICKETS.md §0721 W-IC/W-II/W-IL/W-IO/W-IQ/W-IS — 이벤트 축 확장(turnInto/MDT/Enter/Tab/turnInto조합/SLM) 전부 '기존 어댑터 무회귀' 검증 로그"
  - "260622_notion-clone commit 998a617(FZ004~006 자동발견)·f201cfa(TRN10/19 콜아웃 데이터손실 자동검출→수복)·d57baa3(FE006 자동검출)"
updated: 2026-07-21
owner: 박춘순
---

# 차등 대조 파이프라인 (1단 러너 → 2단 퍼저)

**한 줄**: "사람이 쓰다가 우연히 발견"하던 파리티 갭을, 규칙표를 실제 UI 경로로 **기계가 자동 재생·대조**해 먼저 찾아내는 2단 인프라로 전환한다. 1단은 사람이 미리 측정해둔 규칙표(expected 포함)를 재생하는 러너, 2단은 조합을 자동 생성해 expected 없이 **실물 자체를 오라클로** 클론과 직접 diff하는 퍼저.

## 왜 필요한가

notion 캠페인은 규칙표(`behavior-matrix.json`, 200+행)를 사람이 손으로 real/clone을 눌러보며 채워왔다. 이 방식의 한계 둘:
1. **커버리지가 사람이 짠 시나리오 수만큼만 늘어난다** — 축(블록타입×중첩×형제유무×캐럿위치×키×누른횟수 등)이 조합폭발이라 손으로 다 못 짠다. 실제로 오너가 겪은 "컨테이너 자식+EMPTY+형제有 상태에서 Backspace 2회 필요" 버그를, 사람이 짠 시나리오(`wia_probe.py`)는 여러 세션 동안 못 찾았다.
2. **한 번 측정한 expected는 정적이라** 코드가 나중에 더 정확해져도(예: real 재측정으로 수정) 갱신 안 되면 게이트가 낡는다([[techniques.gate-oracle-staleness]] 참고 — 이 파이프라인이 실제로 그 함정에 걸렸다가 빠져나온 사례를 낳았다).

## 구조

### 1단 — `spec_runner.py`/`spec_lib.py` (규칙표 재생 러너)

`behavior-matrix.json`의 각 행(`id`/`setup`/`event`/`expected`)을 **진짜 UI 경로**로 재생한다 — store 직접주입이 아니라 클릭·타이핑·핸들메뉴 조작으로. 이유: store 직접호출은 UI 레이어 버그(예: "핸들 hover 좌표가 컨테이너 헤더가 아니라 자식 위였다")를 놓친다 — 실제로 이 원칙 덕분에 turnInto 축(TRN14) 확장 때 그런 버그가 잡힌 전례가 있다.

- `CloneAdapter`(clone 9226/5185)와 `RealAdapter`(real 9224, `spec_measure.py`의 기존 검증체 재사용)가 같은 인터페이스로 `setup`→`operate`→관측(`_dump`)을 수행.
- `judge()`가 관측 결과를 `expected`의 표준 체크키(`resultText`/`survivingType`/`deletedIds`/`unchangedTexts`/`cursorBlockId`/`cursorOffset` 등)와 대조해 PASS/FAIL/SKIP.
- `--target clone|real|both`, `--category`(id 접두어 FD/BKSP/TBC/...), `--id`(단일행), `--stamp <이름>`(필수 — 산출물 파일명, `datetime.now()` 금지로 재현성 확보).

### 2단 — `spec_fuzz.py` (조합 생성기, expected 불필요)

1단이 "사람이 미리 답을 채운 문제"만 풀 수 있다는 한계를 깨기 위해, **답 없이 조합을 자동 생성**해 real과 clone에 동시에 재생하고 관측 결과를 **직접 diff**한다 — real이 살아있는 채로 도는 것 자체가 오라클이다(`judge()` 대신 `diff_snapshots()`).

- **생성 축**: blockType × nesting(0~2, 컨테이너=toggle/callout) × targetEmpty × hasPrevSibling × hasNextSibling × caretPos × key(Backspace/Delete/Enter/Tab/turnInto) × presses(1~3).
- **BASELINE + CORE + BREADTH 3단 샘플링**: BASELINE(기존 확정 파리티 재확인용, 2행) → CORE(새 신호축, real 대조 필수 4행) → BREADTH(clone-only 전수, real 예산 밖 — real 상한 5~6행/세션이라 대부분 미대조로 남는다. 이건 결함이 아니라 설계 — `needsConfirmation`으로 정직 분류하고 다음 세션 real 예산 후보로 넘긴다).
- **인프라 재사용 원칙**: setup/operate/observe는 1단(`spec_lib.CloneAdapter`)과 `spec_measure.RealAdapter`(이미 검증된 실물 셋업체)를 그대로 import — 새로 안 만든다. 새 축을 추가할 때도 `spec_lib.py`/`spec_runner.py`는 **무수정**(import만) 원칙을 지켜 기존 축을 절대 회귀시키지 않는다(`--axis <이름>` 신설로 확장).
- **사전조사로 real 낭비 방지**: real 실행 전에 clone-only dry run을 먼저 돌려, clone이 SKIP(예: 어댑터 한계로 관측 불가)인 조합은 애초에 real 대조쌍이 안 만들어지므로 CORE 후보에서 제외하고 다른 조합으로 교체한다(turnInto 축에서 src=callout 7개가 이렇게 걸러졌다).

## ★자기검증 — 이 인프라 자체를 못 믿으면 결과도 못 믿는다

- **known-good/known-bad 재현성**: PASS로 확정된 행을 `--id <행>`으로 **단독 재실행**해도 배치 결과와 동일해야 하고, FAIL로 확정된 행도 마찬가지. 매 축 확장마다 이 확인을 반복한다(예: TRN 확장 시 `--id TRN08`(PASS)·`--id TRN10`(FAIL) 단독 재검증).
- **대조군(BASELINE) 무diff 확인**: 조합 생성기가 새 축을 열 때마다, 이미 파리티가 확정된 조합(BASELINE)을 다시 태워 diff가 0인지 먼저 확인한다 — 생성기 자체가 가짜 diff를 뿜지 않는다는 걸 실물로 재확인하는 절차. 이게 없으면 새 축의 diff가 "진짜 갭"인지 "생성기 버그"인지 구분이 안 된다.
- **★vacuous-pass 함정(치명적 버그, 1단에서 실제 발견)**: `judge()`가 관측 가능한 check가 0개일 때 `all(c["ok"] for c in [])`가 파이썬에서 `True`라 **조용히 PASS로 오판**했다. `expected`가 표준 스키마 대신 커스텀 필드(`_cellNav` 등)만 가진 행이 이 경로로 몇 세션째 "통과"돼 있었다. 수정: **checks=0이면 SKIP** — PASS는 반드시 checks≥1일 때만.
- **가짜 diff 배제(harnessArtifacts 분류)**: diff가 나와도 즉시 "확정 갭"으로 올리지 않는다. 셋업 스키마 자체의 한계(예: 콜아웃이 own-text와 children을 동시에 갖는 상태는 정상 앱 사용으로 절대 발생 안 하는데 하네스가 그렇게 주입해버린 경우)로 인한 diff는 **harnessArtifacts**로 별도 분류하고, 실제 클론 로직 갭(**confirmedCloneGaps**)과 섞지 않는다.

## 실측 성과

- 커버리지 **28.1%(64/228, 인벤토리 직후) → 92.7%(215/232, `spec_coverage.py`)** — 대부분 이 파이프라인의 이벤트 축 확장(turnInto 19행·MDT 15행·Enter/Tab 조합 등)으로.
- **자동검출 확정 갭 예시**: FZ004~006(백스페이스 2회 버그, 998a617 — 손-작성 시나리오가 여러 세션째 못 찾던 것을 조합 생성기가 첫 실행에 발견) · TRN10/19(text/quote→callout 전환 시 텍스트 소실, f201cfa) · FE006(토글 자식 EMPTY Enter 커서 이동, d57baa3).
- **회귀 0** — 매 축 확장이 기존 5개 base 이벤트(FD/BKSP/TAB/STAB/ENTER)에 영향 없음을 매번 재확인(어댑터 확장이 `operate()` 최상단 early-return 분기라 구조적으로 격리됨).

## 함정

- **`conformance-latest.json` 병렬 취약(race)**: `spec_runner.py`가 매 실행마다 이 파일을 "마지막 실행 승자"로 덮어쓴다. 병렬 워커가 동시에 돌리면 in-flight 결과가 유실될 수 있다(실제로 `git checkout --`로 HEAD 복구까지 간 사고 있었음). **정본은 `--stamp` 개별 파일, latest는 참고용으로만** 취급 — 근본 수복(`--no-latest` 옵션 또는 latest 갱신은 오케만)은 아직 티켓 상태.
- **real 예산 상한**: 정책상 세션당 real 실측 5~6행 상한. clone-only BREADTH 조합은 구조적으로 늘 미대조로 남는다 — 이걸 "실패"로 여기지 말고 `needsConfirmation`으로 정직하게 분류해 다음 세션 예산으로 넘길 것.
- **judge()/diff_snapshots() 스키마 불일치는 강제로 억지로 맞추지 마라**: 다른 세션이 다른 오라클 스키마(예: `targetClassAfter`/`menuOpen`)로 측정해둔 행은 어댑터를 확장해도 checks=0으로 SKIP인 채 남는다 — "판정 불가"라는 사실만 확인하고 중단하는 것이 가짜 PASS보다 낫다(정확성 > 범위 원칙).

## 관련

- [[techniques.regression-harness-suite]] — 이 파이프라인이 대체하는 게 아니라 **보완**한다. 정적 게이트(`*_gate.py`)는 "알려진 회귀"를 빠르게 잡고, 이 파이프라인은 "아직 모르는 갭"을 조합적으로 찾는다.
- [[techniques.adversarial-verification]] — 자기검증(known-good/known-bad, BASELINE 무diff) 원칙이 이 기법의 핵심 뿌리.
- [[techniques.gate-oracle-staleness]] — 이 파이프라인이 자동검출한 갭을 오케가 "클론 미구현"으로 오판했다가 워커의 real 재실측으로 반박된 사건에서 도출된 자매 카드.
