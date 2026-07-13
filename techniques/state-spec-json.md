---
id: techniques.state-spec-json
title: 상태 명세 JSON (URL + 도달 절차 재현)
doctype: technique
status: verified
proven_in: [notion]
related: [techniques.rip-css-dump, techniques.cdp-nondestructive-recon]
evidence:
  - "260622_notion-clone/ref/rip/states/*.json — peek_open/popup_date/popup_propmenu/popup_rowmenu/popup_select/title_hover/view_board/view_calendar/view_gallery/view_timeline (10개)"
  - "260622_notion-clone/RIP-PIPELINE.md §6 — '상태 정의: URL+도달 절차(클릭 시퀀스)를 JSON으로 명세해 재현 가능하게'"
updated: 2026-07-13
owner: 박춘순
---

# 상태 명세 JSON (URL + 도달 절차 재현)

**한 줄**: "이 UI 상태를 다시 어떻게 만들지"를 사람 기억이나 스크린샷 캡션에 의존하지 않고, URL + 클릭 시퀀스를 실물/클론 병렬 JSON 스펙으로 남겨서 스크립트가 그대로 재현하게 한다.

## 구조 (실제 파일, ref/rip/states/*.json)
각 스펙 파일은 `real{}` / `clone{}` 블록을 병렬로 가진다:
```json
{
  "real": {
    "cdp": "...", "url": "https://app.notion.com/p/...",
    "root_selector": ".notion-board-view",
    "goto_wait_until": "...",
    "actions": [{"action":"click","selector":"text=보드"}],
    "cleanup": [{"action":"click","selector":"text=표"}]
  },
  "clone": {
    "cdp": "...", "url": "http://localhost:5185/p/t_riptest?v=vrt_board",
    "root_selector": ".bv-board",
    "actions": [...], "cleanup": [...]
  }
}
```
`_verification` 블록에 "누가 언제 왜 root_selector를 수정했나"까지 기록(예: 스코프 오매칭 수정 `root_selector_fix_0713b`).

## 왜 필요한가
- [[techniques.rip-css-dump]]/[[techniques.rip-crawler]] 같은 전수 스캔 도구는 "지금 이 상태에서" 덤프하는 도구다 — **그 상태에 어떻게 도달하는지**는 별도로 명세해야 재현 가능하고 자동화 가능하다.
- `cleanup[]`이 있어서 상태를 만든 뒤 항상 원상복구까지 자동화됨 — [[techniques.cdp-nondestructive-recon]]의 비파괴 원칙을 스펙 레벨에서 강제.
- 실제로 셀렉터 off-by-one 버그(스펙이 의도한 타겟이 아니라 제목 팝업을 잘못 히트)를 이 명세 덕분에 재현·특정·수정할 수 있었다.

## 함정
- 실물 앱 UI가 바뀌면(A/B 테스트, 업데이트) 스펙의 selector/actions가 깨진다 — `_verification` 블록으로 "언제 검증됐는지"를 남겨 신뢰도를 추적해야 함.

## 관련
- [[techniques.rip-css-dump]] — 이 스펙이 상태를 지정해주는 상위 덤프 파이프라인
