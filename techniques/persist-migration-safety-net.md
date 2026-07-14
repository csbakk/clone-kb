---
id: techniques.persist-migration-safety-net
title: 스키마 마이그레이션 안전망 (버전·백업·invariant·게이트)
doctype: technique
status: experimental
proven_in: [notion]
related: [techniques.atomic-localstorage-inject, techniques.regression-harness-suite, techniques.adversarial-verification]
evidence:
  - "260622_notion-clone/clone/src/store/useStore.ts(version/migrate/backup/onRehydrateStorage) + clone/src/lib/storeInvariants.ts + harness/persist_migration_gate.py (15/15) — 커밋 b4a187b"
  - "01-structure-diff.md §2 B-3이 지목한 '트리 리팩터 선결조건'을 이 안전망이 충족"
updated: 2026-07-15
owner: 박춘순
---

# 스키마 마이그레이션 안전망

**한 줄**: 클라이언트 영속 상태(localStorage 등)의 스키마를 바꾸기 전에, **항등 베이스라인 + 변환전 백업 + invariant 검증 + 4단 게이트**를 먼저 깔아 실사용자 데이터를 무손실로 보호하는 재사용 패턴.

## 왜
클론이 성숙하면 데이터 모델을 바꿔야 할 때가 온다(예: flat+depth → children 트리). 그런데 **실사용자 데이터가 이미 그 스키마로 저장**돼 있어, 변환에 버그가 나면 사용자 작업이 날아간다. 대부분의 클론은 스키마 마이그레이션을 한 번도 안 해봐서 version/migrate 인프라 자체가 없다(단일 장애점). 이걸 "실변환 전에" 깔아두는 게 이 기법.

## 4개 구성요소
1. **항등 베이스라인**: 현재(버전없는) 저장 blob을 `version: 1` 베이스라인으로 선언. `migrate(persisted, 0)` = **항등**(그대로 반환) → 기존 데이터가 100% 동일하게 로드됨을 최우선 보장. (zustand persist는 version 미지정 시 내부적으로 `version:0`이라, `version:1` 선언만으로 기존 blob에 migrate가 자동 호출됨.)
2. **변환전 백업**: 실제 버전 상승 시 변환 직전 원본 blob을 `<key>-backup-v<from>`에 스냅샷(최근 1~2개 유지). 항등 경로에선 호출 안 함(변환 없음).
3. **invariant 검증기**: 트리/그래프 무결성 비파괴 검사(고아 노드·depth 연속성·컨테이너 구조·순환). rehydrate 후 1회 돌려 실패 시 경고(자동 롤백은 선택). 변환 결과 검증 + 실패 시 백업 폴백의 판정 근거.
4. **4단 게이트**: ①항등 안전(구형 blob 로드 시 무손실) ②기전(의도적 버전 범프 → migrate 호출·백업 생성 확인) ③폴백(깨진 migrate 주입 → invariant 실패 감지 → 백업 복원) ④invariant 단위(정상 PASS·고아/순환 FAIL).

## 실변환에서 재사용하는 법
`migrate`의 `case 1`에 실 변환 함수를 넣고, 그 안에서 `backup(1, persisted)` 호출 후 `checkInvariants`로 결과 검증 → 게이트 ②③단계를 실변환용으로 바꿔치기만 하면 이번에 증명한 안전성 보증을 그대로 얻는다. **선(先)안전망, 후(後)변환** 순서가 핵심.

## 함정
- 항등 case를 빼먹으면 기존 데이터가 버전 불일치로 **조용히 폐기**된다(zustand는 migrate 없으면 persisted state를 버림). 항등이 최우선.
- 실사용자 데이터에 직접 변환을 돌리기 전, **격리 오리진/포트에서** 게이트로 전 단계를 증명할 것(실데이터 read-only). [[techniques.port-profile-isolation]]와 결합.

## 관련
- [[techniques.atomic-localstorage-inject]] — 반대편(쓰기) 안전. 이건 스키마 변경 안전.
- [[techniques.regression-harness-suite]] — 게이트가 회귀망의 일부.
