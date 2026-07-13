---
id: techniques.atomic-localstorage-inject
title: 원자적 localStorage 주입 (bulk_inject)
doctype: technique
status: verified
proven_in: [notion]
related: [techniques.subagent-fanout-rules, techniques.port-profile-isolation]
evidence:
  - "260622_notion-clone/harness/bulk_inject.py — MERGE_JS 단일 evaluate 실행 + 단일 reload, CLONE_TAB_RE 포트 가드"
  - "260622_notion-clone/HANDOFF.md 2026-06-27 — 'localStorage away-클로버' 버그: build_t2.py의 다중 루프 write→reload 방식이 유휴 세션에서 이전 20-DB 상태로 리셋되던 사고"
updated: 2026-07-13
owner: 박춘순
---

# 원자적 localStorage 주입 (bulk_inject)

**한 줄**: localStorage에 여러 페이지/DB를 심을 때 "쓰고 → 리로드 → 쓰고 → 리로드"를 반복하면 리로드 레이스로 데이터가 유실된다. 전부 메모리에서 합친 뒤 **단 한 번의 write + 단 한 번의 reload**로 끝낸다.

## 문제 상황 (실제 사고)
`build_t2.py`의 원래 방식은 템플릿마다 루프를 돌며 write→reload를 반복 — 유휴 세션 중 이 레이스 때문에 클론이 이전의 20-DB 상태로 조용히 리셋되는 사고가 발생("localStorage away-클로버" 버그, 2026-06-27).

## 어떻게 (harness/bulk_inject.py)
1. `build_t2.TEMPLATES`를 임포트해 모든 페이지 + 모든 DB를 수집.
2. DB는 `id` 기준 dedup(나중 것이 이김, last-wins).
3. 단일 `MERGE_JS` 문자열을 만들어 **한 번의 `pg.evaluate`**로 실행:
   - `localStorage['notion-clone']` 읽기
   - `st.databases`, `st.members`, `st.pages`/`rootOrder` 병합(제목 같은 중복 비-trash 페이지 제거)
   - 부모 row가 사라진 고아 `rowdoc_*` 페이지 정리
   - `st.theme='light'` 강제
   - **한 번의 `localStorage.setItem`**으로 되쓰기
4. **단 한 번의 `pg.reload()`**.
5. 안전장치: `CLONE_TAB_RE = r"^https?://localhost:5185(?:/|\?|#|$)"` — 대상 탭이 진짜 이 프로젝트 포트인지 코드 레벨에서 재확인(다른 포트 탭에 잘못 쓰는 사고 방지, → [[techniques.port-profile-isolation]]과 결합).

## 왜 필요한가
localStorage 자체는 트랜잭션이 없다. 여러 write 사이에 reload/다른 스크립트의 write가 끼어들면 마지막에 이긴 쪽만 남는다 — "합쳐서 한 번에 쓰기"가 유일한 확실한 방어.

## 함정
- 이 패턴은 "여러 소스를 하나로 합친 뒤 한 번에 쓴다"는 일반 원칙이라 localStorage 외에도 적용 가능 — 다른 캠페인에서 상태 저장소가 다르면(IndexedDB 등) 그에 맞게 이식.

## 관련
- [[techniques.subagent-fanout-rules]] — "공유 파일/상태는 병렬 편집 금지" 규칙과 같은 문제의식
