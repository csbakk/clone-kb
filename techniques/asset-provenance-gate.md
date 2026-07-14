---
id: techniques.asset-provenance-gate
title: 자산 출처 게이트 (시각 자산 provenance — 자작 대체 재발방지)
doctype: technique
status: experimental
proven_in: [notion]
related: [techniques.rip-css-dump, techniques.regression-harness-suite, techniques.visual-triage-sheet]
evidence:
  - "260622_notion-clone/harness/asset_provenance.py + ref/asset_provenance.json (등록 94) + ref/_ASSET_DEBT.md (부채 12)"
  - "260622_notion-clone/_WORKLOG 2026-07-14 W-O — 오너 근본 질문('왜 자작 SVG였나')에서 탄생"
updated: 2026-07-14
owner: 박춘순
---

# 자산 출처 게이트 (asset provenance)

**한 줄**: 클론의 모든 시각 자산(SVG 아이콘 등)에 "실측 원본 출처"를 강제하는 정적 게이트 — 출처 없는 자산은 부채 목록으로 노출되고, 신규 무출처 자산·조용한 자작 치환은 게이트 FAIL.

## 왜 (탄생 배경)
"그대로 클론" 원칙(reference-first, 추측 0)이 있어도, **실측이 불가능한 순간**(read-only 제약으로 hover UI 접근 불가 등)에 워커가 "비슷하게 자작"으로 대체하면 기능 게이트는 통과한다 — 오너가 아이콘 차이를 눈으로 발견하고 "왜 자작했나, 매번 '똑같이 해줘'라고 말해야 하나"를 물은 것이 직접 계기. 원칙은 사람이 지키는 게 아니라 **게이트가 지키게** 해야 한다.

## 어떻게
1. **정적 스캔**: `clone/src/data/*Icons.ts` 전수 → SVG path shape 시그니처 추출(비-shape 속성 무시).
2. **자동 대조**: `ref/` 실측 소스(icons 덤프·`*_real*.json`·SVG — clone 캡처는 순환검증이라 제외)와 매칭 → 매칭=`asset_provenance.json` 등록(verified), 미매칭=`_ASSET_DEBT.md` 부채.
3. **`--gate` 모드**(읽기전용): ①대장에도 부채문서에도 없는 신규 무출처 자산 ②등록됐던 자산의 shape이 실측 소스와 더는 안 맞는 "출처 이탈"(조용한 치환) — 둘 다 FAIL. 주요 게이트(video_block_gate 등)의 사전조건으로 편입.
4. **부채 처리 규칙**: 실측 불가 자산은 자작 금지 → placeholder+부채 등록+**오너에게 '실측 개방 요청'**(예: 스크래치에 해당 UI 상태 만들어달라) — notion에서 오너가 영상 업로드로 개방해준 전례.

## 결과 (notion 첫 적용)
- 아이콘 106개 중 94개 자동 등록, **12개 자작/출처불명 부채 발굴**(favorite·caption·download 등 — 사람 눈이 아니라 스캐너가 찾음).
- ⋯메뉴 바꾸기·다운로드 아이콘 자작분을 실측 SVG로 즉시 교체(기존 실측 JSON에 원본이 이미 있었음).
- 파리티 DoD 3층 표준화(CLONE-METHOD.md): 동작(네이티브 경로)+구조(RIP 2층)+**자산 출처** 전부 통과=완료.

## 함정
- 실측 소스 자체가 오염되면(클론 캡처를 소스로 잘못 등록) 순환 검증이 된다 — 소스 필터에서 clone 산출물 제외 필수.
- shape 시그니처만 보므로 색·크기 델타는 못 잡는다 — 그건 RIP 2층(CSS diff) 담당. 역할 분담 명확히.

## 관련
- [[techniques.rip-css-dump]] — 색·기하 델타 담당(이 게이트는 존재·출처 담당)
- [[techniques.regression-harness-suite]] — §함정 "합성 이벤트 거짓 양성"과 같은 뿌리(게이트가 실사용과 다른 경로를 검사하는 문제)
