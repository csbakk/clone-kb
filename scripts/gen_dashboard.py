#!/usr/bin/env python3
"""gen_dashboard — techniques/·cases/·ledger/ 를 파싱해 README.md 대시보드를 재생성.

원칙: 대시보드는 '관리'하지 않고 '파생'한다 — 이 스크립트만이 README를 쓴다.
실행: python3 scripts/gen_dashboard.py  (매 세션 결산 때 오케스트레이터가 실행)
"""
import os, re, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fm(path):
    """frontmatter 최소 파서 (key: value / key: [a, b])"""
    s = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", s, re.S)
    d = {}
    if m:
        for line in m.group(1).splitlines():
            km = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
            if km:
                k, v = km.group(1), km.group(2).strip()
                if v.startswith("["):
                    d[k] = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
                elif v:
                    d[k] = v
    return d

def load(doctype_dir):
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, doctype_dir, "*.md"))):
        d = fm(p); d["_file"] = os.path.relpath(p, ROOT)
        out.append(d)
    return out

techs = load("techniques")
cases = load("cases")
pipes = load("pipelines")

STATUS_ORDER = ["standard", "verified", "experimental", "retired"]
STATUS_KO = {"standard": "정식", "verified": "검증", "experimental": "실험", "retired": "은퇴"}
by_status = {s: [t for t in techs if t.get("status") == s] for s in STATUS_ORDER}

# 원장 최근 항목
ledger_lines = []
for p in sorted(glob.glob(os.path.join(ROOT, "ledger", "*.md")), reverse=True):
    for line in open(p, encoding="utf-8").read().splitlines():
        if line.startswith("| 20"):
            ledger_lines.append(line)
ledger_recent = ledger_lines[:10]

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
L = []
L.append("# clone-kb — 클론 시스템 무기고 (기법 레지스트리 + 평가 원장)")
L.append("")
L.append(f"> **자동 생성 대시보드** (`scripts/gen_dashboard.py`, {now}). 직접 편집 금지 — 카드/원장을 고치고 재생성.")
L.append("> 운영: 평시=AI 직접 커밋(근거 포함) · **승격/은퇴=Issue 제안→오너 승인** · status=standard만 skills/ 보유 가능(강등 시 스킬도 제거).")
L.append("")
L.append("## 기법 상태 분포")
L.append("")
L.append("```mermaid")
L.append("pie showData")
L.append(f'    title 기법 {len(techs)}장')
for s in STATUS_ORDER:
    if by_status[s]:
        L.append(f'    "{STATUS_KO[s]} ({s})" : {len(by_status[s])}')
L.append("```")
L.append("")
L.append("## 기법 카드")
L.append("")
for s in STATUS_ORDER:
    if not by_status[s]:
        continue
    L.append(f"### {STATUS_KO[s]} ({s}) — {len(by_status[s])}")
    L.append("")
    L.append("| 기법 | 실증 | 카드 |")
    L.append("|---|---|---|")
    for t in by_status[s]:
        proven = ", ".join(t.get("proven_in", [])) or "—"
        title = t.get("title", t.get("id", "?"))
        L.append(f"| {title} | {proven} | [{t['_file']}]({t['_file']}) |")
    L.append("")
L.append("## 파이프라인 (조립도)")
L.append("")
for p in pipes:
    L.append(f"- **{p.get('title', p.get('id'))}** — [{p['_file']}]({p['_file']})")
L.append("")
L.append("## 캠페인 진행 (cases/)")
L.append("")
L.append("| 캠페인 | 상태 | 사례 |")
L.append("|---|---|---|")
for c in cases:
    L.append(f"| {c.get('title', c.get('id'))} | {c.get('status', '—')} | [{c['_file']}]({c['_file']}) |")
L.append("")
L.append("## 최근 평가 원장 (ledger/)")
L.append("")
if ledger_recent:
    L.append("| 날짜 | 프로젝트 | 기법 | 판정 | 증거 |")
    L.append("|---|---|---|---|---|")
    L.extend(ledger_recent)
else:
    L.append("_아직 원장 항목 없음_")
L.append("")
L.append("## 소비 방법 (에이전트)")
L.append("")
L.append("1. 캠페인 시작 시 `index.md` → 관련 카드만 로드 (스킬 로딩 패턴)")
L.append("2. 세션 결산 시 사용 기법의 판정을 `ledger/`에 append + `python3 scripts/gen_dashboard.py`")
L.append("3. 새 기법 = experimental 카드로 등록 → 2프로젝트 실증 시 verified → Issue 승인으로 standard(스킬 포장) → 대체 시 retired(`superseded_by`)")

open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"README.md 재생성 — 기법 {len(techs)} (" + ", ".join(f"{STATUS_KO[s]} {len(by_status[s])}" for s in STATUS_ORDER) + ")")
