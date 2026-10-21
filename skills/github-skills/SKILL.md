---
name: github-skills
description: 사용자의 GitHub 저장소(wlscksdjs-bit/skills 등)에서 스킬을 검색, 조회하거나 필요 시 온디맨드(on-demand)로 스킬을 꺼내와 실행할 때 사용합니다. "깃허브 스킬 보여줘", "스킬 꺼내줘", "깃허브에서 스킬 가져와" 등의 요청에 트리거됩니다.
---

# GitHub Skills On-Demand Loader

사용자의 개인 GitHub 저장소(`wlscksdjs-bit/skills`) 및 오픈소스 GitHub 레포지토리에 저장된 스킬을 로컬 컨텍스트 낭비 없이 필요할 때만 온디맨드로 불러와 사용하는 스킬입니다.

## 원격 저장소 정보
- 기본 스킬 저장소: `wlscksdjs-bit/skills`
- 로컬 작업 경로: `C:\Users\Administrator\.gemini\antigravity\scratch\skills`

## 주요 동작 절차

### 1. GitHub 스킬 목록 조회
사용자가 GitHub에 등록된 스킬을 확인하고자 할 때:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\Administrator\.gemini\antigravity\scratch\skills\manage-skills.ps1" list
```

### 2. 1회성 온디맨드 스킬 로드 (영구 설치 없이 즉시 실행)
사용자가 특정 스킬을 지금 당장 쓰고 싶어할 때:
```cmd
npx.cmd skills use wlscksdjs-bit/skills@<skill-name>
```
위 명령이 출력하는 `<SKILL.md>` 지침과 다운로드된 `Supporting files` 경로를 참조하여 해당 스킬 작업을 즉시 수행합니다.

### 3. 프로젝트/에이전트에 임시 설치 및 제거
스킬을 일정 기간 프로젝트에서 계속 사용해야 할 때:
```cmd
# 설치
npx.cmd skills add wlscksdjs-bit/skills --skill <skill-name> --agent antigravity

# 작업 완료 후 로컬 제거 (토큰 절약)
npx.cmd skills remove <skill-name> --agent antigravity -y
```

### 4. 로컬 스킬을 GitHub 저장소에 내보내기/동기화
새로 작성한 로컬 스킬을 GitHub으로 관리하고 싶을 때:
```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\Administrator\.gemini\antigravity\scratch\skills\manage-skills.ps1" export <skill-name>
powershell -ExecutionPolicy Bypass -File "C:\Users\Administrator\.gemini\antigravity\scratch\skills\manage-skills.ps1" push "add <skill-name>"
```
