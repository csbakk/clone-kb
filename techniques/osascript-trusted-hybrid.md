---
id: techniques.osascript-trusted-hybrid
title: osascript 트러스티드 입력 하이브리드 (한글 IME 우회)
doctype: technique
status: verified
proven_in: [notion]
related: [techniques.cdp-nondestructive-recon, techniques.port-profile-isolation]
evidence:
  - "260622_notion-clone/harness/seq.py — --backend cdp|trusted 스위치, _osa/trusted_key/trusted_type/trusted_paste 헬퍼"
  - "260622_notion-clone/ref/BEHAVIOR-PARITY.md 헤더 — 포커스/캐럿/내비/캡처=CDP, 트러스티드 키=osascript, 한글=pbcopy→Cmd+V"
  - "__obsidian/wiki/concepts/입력자동화-레이어-동작재현.md §5.3 — 2026-06-26 돌파: CDP 언트러스티드로 3회 실패했던 노션 슬래시메뉴를 이 하이브리드로 해결(_BLOCKED B4)"
updated: 2026-07-13
owner: 박춘순
---

# osascript 트러스티드 입력 하이브리드 (한글 IME 우회)

**한 줄**: Playwright의 키 입력은 브라우저 입장에서 "untrusted 이벤트"라 일부 네이티브 동작(슬래시 메뉴, IME)을 못 깨운다. 포커스/캐럿/네비게이션/캡처는 CDP로, **실제 키 입력이 필요한 순간만** macOS `osascript`(System Events)로 전환하고, 한글은 클립보드 붙여넣기로 IME 자체를 우회한다.

## 실감도 사다리 (입력자동화-레이어-동작재현.md 정의)
① JS 이벤트 디스패치(untrusted) → ② CDP/Playwright(페이지엔 trusted, IME는 약함) → ③ OS 레벨 주입(trusted+IME+실제 커서, **이 기법**) → ④ 하드웨어 HID(불필요 판단).

## 어떻게
- 포커스·캐럿 위치·네비게이션·캡처: CDP(Playwright `connect_over_cdp`, 포트 9224).
- 실제 키 입력: `osascript`로 Chrome을 activate → 딜레이 → System Events `key code`/`keystroke`. 키코드: Enter=36, Esc=53, Backspace=51, Tab=48.
- 한글: `pbcopy`로 클립보드에 넣고 Cmd+V로 붙여넣기 — IME 조합 자체를 건드리지 않음.
- `harness/seq.py --backend cdp|trusted` 스위치, `focusempty`(빈 노션 텍스트 블록만 타겟팅), 포커스 실패 시 abort 가드.

## 실증 성과
2026-06-26 돌파 — 노션의 `/` 슬래시 메뉴는 CDP untrusted 입력으로 3회 연속 실패했던 항목(`_BLOCKED B4`)이었는데, 이 하이브리드로 해결(추천/기본블록/헤딩1-4 메뉴 정상 오픈, 한글 클립보드 붙여넣기 확인) → B4 🟢 해결.

## 알려진 한계 (B6, 미해결 잔여 리스크)
멀티스텝 트러스티드 시퀀스(포커스+Enter+타이핑+캐럿+Enter+복원)를 연달아 실행하면 OS 포커스가 페이지 제목으로 튀는 사고가 2회 발생(자동 복구는 됨). 완화책: osascript 키 입력 전에 CDP 마우스 클릭(`click_box`)으로 포커스를 한 번 더 강제. 정책: split/merge 같은 멀티스텝 편집은 **클론에서만**(결정적) 검증하고, 실물 노션에 대한 트러스티드 입력은 짧은 시퀀스로 제한.

## 관련
- [[techniques.cdp-nondestructive-recon]] — 이 하이브리드가 결합되는 상위 정찰/조작 원칙
