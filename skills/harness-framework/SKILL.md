---
name: harness-framework
description: AI 에이전트 기반의 안전하고 체계적인 소프트웨어 개발을 위한 Harness Framework 스킬. 프로젝트 가드레일 문서(CLAUDE.md/AGENTS.md, PRD, ARCHITECTURE, ADR, UI_GUIDE) 초기화, Task 인터뷰 및 Phase/Step 단위 작업 분해(phases/index.json, stepN.md), 자가 교정 및 2단계 커밋 기반의 자동화 실행(scripts/execute.py), 아키텍처/스택/테스트 준수 여부를 감사하는 리뷰(/review)를 수행할 때 사용한다.
---

# Harness Framework

Harness Framework는 AI 코딩 에이전트가 환각이나 아키텍처 일탈 없이 명확한 가드레일 안에서 안전하고 자율적으로 소프트웨어를 개발할 수 있도록 돕는 프레임워크입니다.

## 핵심 구성 요소

1. **가드레일 & 스펙 문서 (`docs/`, `CLAUDE.md` / `AGENTS.md`)**:
   - `CLAUDE.md` / `AGENTS.md`: CRITICAL 가드레일, 기술 스택, TDD 원칙, 빌드/테스트 명령어
   - `docs/PRD.md`: 제품 요구사항 정의서 (목표, 사용자, 핵심 기능, MVP 제외 사항)
   - `docs/ARCHITECTURE.md`: 디렉토리 구조, 디자인 패턴, 데이터 흐름, 상태 관리
   - `docs/ADR.md`: 아키텍처 결정 기록(선택 이유, 포기한 트레이드오프)
   - `docs/UI_GUIDE.md`: UI 디자인 원칙, AI 슬롭 안티패턴(글로우/블러/보라색 템플릿 금지), 색상, 컴포넌트

2. **Phase & Step 계획 (`phases/{task-name}/`)**:
   - `index.json`: 단계별 상태(`pending`, `completed`, `error`, `blocked`) 및 산출물 `summary` 기록
   - `step0.md`, `step1.md`, ...: 읽어야 할 파일, 작업 지시, AC(Acceptance Criteria), 검증 절차, 금지사항

3. **자동화 실행 엔진 (`scripts/execute.py`)**:
   - 브랜치 자동 생성 (`feat-{task-name}`)
   - 가드레일 문서 및 이전 step의 summary 컨텍스트 자동 누적 주입
   - AC 검증 및 실패 시 최대 3회 자가 교정
   - 코드 변경(`feat`)과 메타데이터(`chore`) 2단계 자동 커밋

4. **아키텍처 감사 및 리뷰 (`/review`)**:
   - ARCHITECTURE, ADR, CLAUDE.md, 테스트 유무, 빌드 통과 여부 테이블 감사

---

## 사용 방법 & 워크플로우

### 1. 프로젝트 초기화 (`harness init`)
사용자가 "현재 프로젝트에 하네스 세팅해줘", "하네스 프레임워크 초기화해줘"라고 요청하면:
```bash
python C:\Users\JIN\.harness_framework\scripts\init_harness.py .
```
- 프로젝트 루트에 `docs/`, `scripts/`, `phases/`, `CLAUDE.md`, `.claude/` 가 자동 생성됩니다.

### 2. Task 인터뷰 & 스펙 수립 (`harness plan`)
1. 프로젝트의 `CLAUDE.md`와 `docs/*.md`를 점검하고 누락된 내용을 사용자 인터뷰를 통해 채웁니다.
2. 새 작업(Task)에 대해 아래 사항을 확인합니다:
   - 작업 목표 및 범위
   - 제외할 사항 (Out of scope)
   - 사용할 기술 및 컴포넌트

### 3. Phase & Step 분해
`phases/{task-name}/` 디렉토리를 생성하고 다음을 작성합니다:
- `index.json`:
  ```json
  {
    "project": "<프로젝트명>",
    "phase": "<task-name>",
    "steps": [
      { "step": 0, "name": "setup", "status": "pending" },
      { "step": 1, "name": "core-logic", "status": "pending" }
    ]
  }
  ```
- `step0.md`, `step1.md`: 읽을 파일, 작업 지시, AC, 검증, 금지사항 정의

### 4. 실행 및 자가 교정 (`harness execute`)
```bash
python scripts/execute.py {task-name}
```
또는 Antigravity 에이전트가 각 step을 순차적으로 수행하면서 AC를 검증하고 `index.json`을 업데이트합니다.

### 5. 아키텍처 리뷰 (`harness review`)
구현 완료 후 `/review` 체크리스트를 실행하여 아키텍처/가드레일 준수 여부를 검증합니다.
