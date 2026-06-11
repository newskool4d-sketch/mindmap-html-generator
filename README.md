# mindmap-html-generator

한국어 HTML 마인드맵 생성 스킬. JSON 스펙 → 단일 HTML 파일 자동 빌드, 13개 교과 테마,
교과용·발표용·퀴즈형 모드, 데스크톱 우선 레이아웃.

이 저장소는 **Claude Code와 Codex CLI 양쪽에 배포되는 스킬의 단일 출처(single source of truth)**다.
모든 수정은 이 저장소에서 먼저 하고, 아래 동기화 절차로 각 플랫폼에 배포한다.

## 저장소 구조

```
SKILL.md                      ← Claude Code용 스킬 정의 (한국어)
assets/
  base-mindmap-template.html  ← [코어] 공용 HTML 템플릿
scripts/
  build_mindmap.py            ← [코어] JSON 스펙 → HTML 빌더
references/
  output-modes.md             ← [코어] 모드별 정량 스펙 (교과용·발표용·퀴즈형)
  subject-themes.md           ← [코어] 13개 교과 테마 + 아이콘 추천
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

## 배포 대상

| 플랫폼 | 배포 경로 |
|--------|----------|
| Claude Code | `~/.claude/skills/mindmap-html-generator/` (이 저장소의 클론 자체) |
| Codex CLI | `~/.codex/skills/mindmap-html-generator/` (수동 동기화) |

## 동기화 절차 (수정 → 배포)

1. 이 저장소(= `~/.claude/skills/mindmap-html-generator/`)에서 수정·커밋한다.
   - Claude Code 쪽은 클론 자체가 배포본이므로 이것으로 배포 완료.
2. Codex 쪽으로 복사한다 (한글 경로이므로 Python 사용):

```powershell
python -c "
import shutil
from pathlib import Path
src = Path(r'C:/Users/홍주형/.claude/skills/mindmap-html-generator')
dst = Path(r'C:/Users/홍주형/.codex/skills/mindmap-html-generator')
# 코어 자산
for f in ['assets/base-mindmap-template.html', 'scripts/build_mindmap.py',
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

- 루트 `SKILL.md`(Claude)와 `adapters/codex/SKILL.md`는 **내용상 같은 v2 워크플로우**를 설명한다.
  규칙(브랜치 수, 승인 규칙, 테마 표 등)을 바꾸면 두 파일 모두 갱신할 것.
- Codex SKILL.md에만 있는 것: 인접 스킬 핸드오프(`board-writing-generator` 등), `apply_patch` 지침,
  `common-operating-rules` 참조 — 이들은 Codex 환경 전용이므로 Claude SKILL.md에 넣지 말 것.
- 모드 명칭 표준은 `교과용 / 발표용 / 퀴즈형` (v1의 `교육용` 표기는 폐기됨).

## 버전 이력

- **v2** — JSON 빌더(`build_mindmap.py`), 모드 3종 정량 스펙, 교과 테마 13종, 인쇄·접근성, 퀴즈 블록
- **v1** — 최초 릴리스 (수동 템플릿 편집, 교과 테마·빌더 없음)
