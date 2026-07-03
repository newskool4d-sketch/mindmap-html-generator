# mindmap-html-generator

한국어 HTML 마인드맵 생성 스킬. JSON 스펙 → 단일 HTML 파일 자동 빌드, 13개 교과 테마,
교과용·발표용·퀴즈형 모드, v3 교육 설계 메타데이터, 데스크톱 우선 레이아웃.

이 저장소는 **Claude Code와 Codex CLI 양쪽에 배포되는 스킬의 단일 출처(single source of truth)**다.
모든 수정은 이 저장소에서 먼저 하고, 아래 동기화 절차로 각 플랫폼에 배포한다.

## 저장소 구조

```
DESIGN.md                     ← [코어] 생성 HTML 시각 디자인 계약
SKILL.md                      ← Claude Code용 스킬 정의 (한국어)
assets/
  base-mindmap-template.html  ← [코어] 공용 HTML 템플릿
scripts/
  build_mindmap.py            ← [코어] JSON 스펙 → HTML 빌더
references/
  educational-design.md      ← [코어] v3 교육 설계 메타데이터 계약
  branch-archetypes.md       ← [코어] 교과·수업 목적별 브랜치 기본 구조
  output-modes.md             ← [코어] 모드별 정량 스펙 (교과용·발표용·퀴즈형)
  subject-themes.md           ← [코어] 13개 교과 테마 + 아이콘 추천
tests/
  test_build_mindmap.py       ← [검증] stdlib 기반 빌더 회귀 테스트
  fixtures/                   ← [검증] v2/v3/오류/퀴즈 fixture
    current-v2-valid.json
    v3-pedagogy.json
    quiz-approved.json
    quiz-mode-no-quiz.json
    invalid-*.json
adapters/
  codex/
    SKILL.md                  ← Codex CLI용 스킬 정의 (영어, 핸드오프·apply_patch 지침 포함)
    agents/openai.yaml        ← Codex 인터페이스 메타데이터
    references/
      layout-interaction-rules.md   ← Codex 전용 상세 규칙
      routing-smoke-test.md         ← 트리거 경계 회귀 체크
```

- **[코어]** 파일은 두 플랫폼이 공유한다. 수정 시 양쪽 모두 재배포해야 한다.
- `adapters/codex/`는 Codex 배포본에만 들어가는 파일이다. Claude 배포본에는 포함하지 않는다.
- 시각 디자인은 루트 `DESIGN.md`가 단일 계약이다. 템플릿 스타일을 바꿀 때는 먼저 `DESIGN.md`를 읽고, 필요한 토큰·상태·QA 규칙을 문서에 반영한 뒤 템플릿을 수정한다.

## 배포 대상

| 플랫폼 | 배포 경로 |
|--------|----------|
| Claude Code | `~/.claude/skills/mindmap-html-generator/` (이 저장소의 클론 자체) |
| Codex CLI | `~/.codex/skills/mindmap-html-generator/` (수동 동기화) |

## 릴리스 체크

수정 후 배포 전, 이 저장소에서 먼저 실행한다.

```powershell
python -m py_compile scripts/build_mindmap.py
python tests/test_build_mindmap.py
python scripts/build_mindmap.py tests/fixtures/current-v2-valid.json -o .omo/evidence/readme-release/out/v2
python scripts/build_mindmap.py tests/fixtures/v3-pedagogy.json -o .omo/evidence/readme-release/out/v3
python scripts/build_mindmap.py tests/fixtures/quiz-approved.json -o .omo/evidence/readme-release/out/quiz
```

문서 회귀 확인:

- `adapters/codex/references/routing-smoke-test.md`의 must/must-not 트리거 목록 확인
- `DESIGN.md`에 `classroom whiteboard workspace`, 브랜드 클론 금지, visual QA 기준이 유지되는지 확인
- `references/output-modes.md`에서 `mode`와 `pedagogy.lesson_purpose`가 분리되어 있는지 확인
- 생성 HTML에 `{{` placeholder가 남지 않았는지 확인
- 템플릿/시각 변경 후에는 실제 브라우저에서 1280px 이상, 768px, 375-390px, reduced motion, print, branch/quiz 상태를 캡처해 evidence에 남긴다.

## 동기화 절차 (수정 → 배포)

1. 이 저장소(= `~/.claude/skills/mindmap-html-generator/`)에서 수정·검증·커밋한다.
   - Claude Code 쪽은 클론 자체가 배포본이므로 이것으로 배포 완료.
2. 사용자가 Codex 배포 동기화를 명시적으로 실행할 때만 Codex 쪽으로 복사한다
   (한글 경로이므로 Python 사용):

```powershell
python -c "
import shutil
from pathlib import Path
src = Path(r'C:/Users/홍주형/.claude/skills/mindmap-html-generator')
dst = Path(r'C:/Users/홍주형/.codex/skills/mindmap-html-generator')
# 코어 자산
for f in ['DESIGN.md', 'assets/base-mindmap-template.html', 'scripts/build_mindmap.py',
          'references/educational-design.md', 'references/branch-archetypes.md',
          'references/output-modes.md', 'references/subject-themes.md']:
    (dst / f).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src / f, dst / f)
# Codex 어댑터
ad = src / 'adapters' / 'codex'
for f in ['SKILL.md', 'agents/openai.yaml',
          'references/layout-interaction-rules.md', 'references/routing-smoke-test.md']:
    (dst / f).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ad / f, dst / f)
print('sync done')
"
```

3. 배포 후 검증:
   - `python ~/.codex/skills/mindmap-html-generator/scripts/build_mindmap.py <spec.json>` 스모크 테스트
   - `adapters/codex/references/routing-smoke-test.md`의 must/must-not 트리거 목록 확인

## 수정 시 주의

- 루트 `SKILL.md`(Claude)와 `adapters/codex/SKILL.md`는 **내용상 같은 v3 워크플로우**를 설명한다.
  규칙(브랜치 수, 승인 규칙, 테마 표 등)을 바꾸면 두 파일 모두 갱신할 것.
- Codex SKILL.md에만 있는 것: 인접 스킬 핸드오프(`board-writing-generator` 등), `apply_patch` 지침,
  `common-operating-rules` 참조 — 이들은 Codex 환경 전용이므로 Claude SKILL.md에 넣지 말 것.
- 모드 명칭 표준은 `교과용 / 발표용 / 퀴즈형` (v1의 `교육용` 표기는 폐기됨).
- 수업 목적 표준은 `도입 / 정리 / 복습 / 평가 / 탐구`이며, 렌더링 모드와 섞지 말 것.
- 퀴즈·애니메이션은 계속 명시적 승인 전에는 추가하지 말 것.
- 기본 시각 방향은 `DESIGN.md`의 **classroom whiteboard workspace**다. Miro/IBM/Apple/Cursor/Airbnb 계열 레퍼런스는 영감과 가중치일 뿐이며, 팔레트·로고·제품 UI·마케팅 구성을 복제하지 말 것.
- Dell 1996 retro, Nike campaign, Voltagent dark developer chrome, marketplace/search/card UI, bokeh/orbs, generic AI gradients는 기본 디자인 방향이 아니다.

## 생성물 정리

- 커밋 대상: 스킬 정의, 템플릿, 빌더, references, tests, fixtures, 필요한 evidence 요약 문서.
- 커밋 제외: `scripts/__pycache__/`, `.pyc`, 임시 생성 HTML, `.omo/ulw-research/.../out`, 검증용 대량 출력물.
- `.omo/evidence/.../out` 아래 생성 HTML은 검증 근거로만 사용하고, 릴리스 산출물로 복사하지 않는다.

## 버전 이력

- **v3** — 선택 `pedagogy` 메타데이터, 교육 설계 기준, 교과·수업 목적별 브랜치 archetype, v2/v3 fixture 회귀 테스트, 접근성·리플로우 보강
- **v2** — JSON 빌더(`build_mindmap.py`), 모드 3종 정량 스펙, 교과 테마 13종, 인쇄·접근성, 퀴즈 블록
- **v1** — 최초 릴리스 (수동 템플릿 편집, 교과 테마·빌더 없음)
