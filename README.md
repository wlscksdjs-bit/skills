# Agent Skills Repository (@wlscksdjs-bit/skills)

AI 에이전트(Antigravity, Claude Code 등)를 위한 맞춤형 스킬 모음 저장소입니다.  
수백 개의 스킬을 로컬에 상시 로드하여 발생하는 **컨텍스트 토큰 낭비(Token Overhead)** 및 **스킬 누락(Context Budget Limit)** 문제를 방지하고, 필요한 스킬만 GitHub에서 온디맨드(On-Demand)로 꺼내 쓸 수 있도록 관리합니다.

---

## 🚀 빠른 시작 (온디맨드 사용법)

### 1. 설치 없이 1회성으로 스킬 사용 (`skills use`)
로컬 컴퓨터에 스킬을 영구 설치하지 않고, 현재 대화 세션에만 임시로 불러와 즉시 실행합니다:
```bash
npx skills use wlscksdjs-bit/skills@<스킬이름>
```

### 2. 현재 프로젝트에 임시 설치 (`skills add`)
특정 프로젝트에서 계속 사용할 스킬만 골라서 설치합니다:
```bash
npx skills add wlscksdjs-bit/skills --skill <스킬이름> --agent antigravity
```

### 3. 작업 완료 후 스킬 제거 (`skills remove`)
작업이 끝난 후 스킬을 제거하여 에이전트 컨텍스트를 가볍게 유지합니다:
```bash
npx skills remove <스킬이름> --agent antigravity -y
```

---

## 🛠️ 간편 관리 스크립트 (`manage-skills.ps1`)

PowerShell 터미널에서 아래 명령어로 스킬 목록 조회, 가져오기, 업로드를 원클릭으로 처리할 수 있습니다:

```powershell
# GitHub에 등록된 스킬 목록 및 로컬 상태 확인
.\manage-skills.ps1 list

# 1회성 온디맨드 실행
.\manage-skills.ps1 use <스킬이름>

# 로컬 에이전트에 설치
.\manage-skills.ps1 add <스킬이름>

# 로컬 에이전트에서 제거 (토큰 절약)
.\manage-skills.ps1 remove <스킬이름>

# 로컬에 있는 스킬을 이 저장소로 내보내기 (백업/동기화)
.\manage-skills.ps1 export <로컬스킬이름>

# 변경 사항을 GitHub에 푸시
.\manage-skills.ps1 push [커밋메시지]
```

---

## 📂 디렉토리 구조

```text
skills/
├── .gitignore
├── README.md
├── manage-skills.ps1        # 스킬 관리 스크립트
└── skills/                  # 스킬 패키지 폴더
    └── <skill-name>/
        ├── SKILL.md         # 메타데이터 (YAML Frontmatter) 및 지침
        ├── references/      # 참고 문서 (필요 시에만 로드)
        └── scripts/         # 보조 실행 스크립트
```
