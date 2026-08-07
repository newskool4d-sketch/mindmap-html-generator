# Mindmap HTML Generator v3.1 리팩토링·고도화 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 검증된 v3 기반 위에서 (a) 낡은 문서·취약한 저장소 위생·빌더 구조를 리팩토링하고, (b) 기존 design-next 계획(D1~D5)을 실행 가능한 과업으로 완수하며, (c) 사용자 승인된 디자인 진화 — **모든 교과 테마에서 6색 이상 멀티 컬러 노트 + 절제된 스큐어모피즘** — 를 템플릿에 반영한다.

**Architecture:** 단일 파일 빌더(`scripts/build_mindmap.py`) 원칙을 유지한 채 내부만 순수 렌더 함수와 I/O 래퍼로 분리한다. 템플릿은 단일 HTML(인라인 CSS/JS) 계약을 유지하고, 시각 변경은 `DESIGN.md` 토큰 계약을 먼저 실측과 일치시킨 뒤(Task 1) → 계약에 신규 방향을 추가하고(Task 8 Step 1) → 템플릿을 수정(Task 8)하는 순서로 진행한다. 검증은 stdlib unittest(서브프로세스 E2E + in-process 단위 테스트 + 템플릿 계약 테스트)와 Playwright visual QA 스크립트 승격으로 이원화한다.

**Tech Stack:** Python 3 stdlib only(신규 의존성 금지), 단일 HTML 템플릿, Node + Playwright(기존 설치본만 사용 — 신규 설치는 사용자 승인 필요).

## Global Constraints

- 빌더는 **stdlib 전용** 유지 — 신규 패키지·의존성 추가 금지.
- `scripts/build_mindmap.py`는 **단일 파일** 유지 — 모듈 분리 금지.
- 산출물은 **단일 HTML 파일**(CSS/JS 인라인) 유지.
- 브랜치 최대 **8개**, 모드 명칭 `교과용 / 발표용 / 퀴즈형`, 수업 목적 `도입 / 정리 / 복습 / 평가 / 탐구` — 표기 변경 금지.
- CLI 출력 접두사 `[완료] / [오류] / [경고]` 및 기존 한국어 메시지 문자열은 하위 호환 유지 (기존 서브프로세스 테스트가 문자열을 검증함).
- 퀴즈·애니메이션은 명시 승인 후에만 — 저장소 내부 QA fixture는 검증 목적으로 quiz 키 사용 허용(기존 `quiz-approved.json` 선례).
- 디자인은 `DESIGN.md`의 **classroom whiteboard workspace** 계약 준수, 브랜드 클론(Miro/IBM/Apple/Cursor/Airbnb) 금지. v3.1에서 사용자 승인으로 **절제된 스큐어모피즘 + 전 테마 6색 이상 노트 팔레트**로 확장하되, 스큐어모피즘 큐는 CSS 전용(외부 텍스처 이미지 금지), 한글 텍스트 대비 유지, 인쇄 시 평면화를 지킨다.
- 모든 파일 쓰기는 **UTF-8 명시**, 한글 경로 조작은 Python 사용.
- 커밋만 하고 **push는 사용자 확인 후에만**. Codex 동기화(`~/.codex/skills/...`)는 사용자가 명시 요청할 때만 실행.
- Playwright 미가용 시 브라우저 QA는 중단하고 "렌더링 미검증"으로 보고 — 임의 설치 금지.

## 파일 구조 (생성·수정 맵)

| 파일 | 작업 | 책임 |
|------|------|------|
| `SKILL.md` | 수정 | 낡은 43MB 캐시 메모 제거 (T1), 스큐어모피즘·멀티 컬러 한 줄 반영 (T8) |
| `DESIGN.md` | 수정 | 토큰 표를 템플릿 실측과 일치 (T1, D1), 스큐어모피즘·멀티 컬러 계약 추가 (T8) |
| `assets/base-mindmap-template.html` | 수정 | 스큐어모피즘 CSS + 테마 멀티 컬러 상속 (T8) |
| `.gitignore` | 수정 | 화이트리스트 일반화 + 테스트 스크래치 제외 (D5) |
| `tests/test_build_mindmap.py` | 수정 | 스크래치 경로 이전, in-process 단위 테스트 추가, 신규 fixture 테스트 |
| `scripts/build_mindmap.py` | 수정 | `SpecError` + `render_html()` 분리 (CLI 동작 불변) |
| `tests/fixtures/pedagogy-single-field.json` | 생성 | D4 부분 pedagogy 검증 |
| `tests/fixtures/design-long-title.json` | 생성 | D2 장문 한글 제목 검증 |
| `tests/fixtures/design-vocab-heavy.json` | 생성 | D2 어휘 중심 검증 |
| `tests/fixtures/design-state-showcase.json` | 생성 | D3 전 상태 showcase |
| `tests/visual-qa.mjs` | 이동 | evidence 임시 경로의 QA 스크립트를 정식 검증 도구로 승격 |
| `README.md` | 수정 | 구조 트리·릴리스 체크 최신화, 버전 이력 v3.1 |

---

### Task 1: 문서 정합성 — 낡은 메모 제거 + DESIGN.md 토큰 표 실측 정렬 (D1 문서부)

**Files:**
- Modify: `SKILL.md:18`
- Modify: `DESIGN.md` (§2 Palette 표, §4 Spacing 표, §7 Depth 표, §6 뒤에 신규 토큰 절)

**Interfaces:**
- Consumes: 없음 (문서만)
- Produces: 이후 모든 템플릿 작업이 참조할 정확한 토큰 계약. 토큰 정식 명칭: `--surface-note-1`~`--surface-note-8`, `--radius-board|node|panel|quiz|pill`, `--motion-expand`, `--motion-control`, `--shadow-panel`, `--border-on-note`, `--space-7`.

- [ ] **Step 1: SKILL.md의 낡은 캐시 비대 메모 삭제**

실측(2026-08-07): `.omo` 368K + `.git` 433K ≈ 0.8MB — "약 43MB" 메모는 이미 정리된 상태를 반영하지 못한 낡은 정보. 18행에서 아래 줄을 삭제:

```
> 참고: 이 폴더의 `.omo`·`.git` 캐시가 약 43MB로 비대함 — 스킬 로직과 무관한 별도 정리 대상.
```

- [ ] **Step 2: DESIGN.md Palette 표의 Note 토큰명을 실측과 일치**

기존 행:

```markdown
| Note 1-8 | `--note-1` to `--note-8` | soft subject-compatible tints | Branch note surfaces |
```

교체:

```markdown
| Note 1-8 | `--surface-note-1` to `--surface-note-8` | soft subject-compatible tints | Branch note surfaces |
| Border on note | `--border-on-note` | translucent white | Branch note inner border |
```

- [ ] **Step 3: DESIGN.md Spacing 표에 `--space-7` 추가**

`--space-6` 행과 `--space-8` 행 사이에 삽입:

```markdown
| `--space-7` | 28px | Wide card inner spacing |
```

- [ ] **Step 4: DESIGN.md Depth 표 실측 정렬**

기존 행:

```markdown
| Flat | `--shadow-none` | Print and connector SVG |
```

교체 (템플릿에 `--shadow-none` 토큰은 없고 print에서 `box-shadow: none` 직접 지정):

```markdown
| Flat | (`box-shadow: none` 직접 지정 — print/connector 전용 one-off) | Print and connector SVG |
| Panel | `--shadow-panel` | Pedagogy panel separation |
```

- [ ] **Step 5: DESIGN.md §6 Motion 뒤에 토큰 실측 절 추가**

§7 Depth 앞에 삽입:

```markdown
### Motion & Radius Tokens (template-implemented)

| Token | Value | Usage |
| --- | --- | --- |
| `--motion-expand` | `max-height 0.35s ease, padding 0.35s ease` | Branch expand/collapse |
| `--motion-control` | 0.16s ease-out multi-property | Control hover/active/focus |
| `--radius-board` | 30px | Main board |
| `--radius-node` | 24px | Branch notes / center |
| `--radius-panel` | 18px | Pedagogy panel |
| `--radius-quiz` | 14px | Quiz block |
| `--radius-pill` | 999px | Toggle pill |

### Legacy Alias Layer

Subject themes override the legacy tokens `--bg`, `--panel`, `--text`, `--muted`, `--line`, `--center1/2`, `--card1`-`--card8`, `--shadow`. The semantic tokens above consume them via `var()` aliases (e.g. `--surface-canvas: var(--bg)`). This alias layer is the intentional theme-override surface; new CSS must reference the semantic tokens, never the legacy names directly.
```

- [ ] **Step 6: 정합성 검증 (grep)**

```bash
grep -n "43MB" SKILL.md; grep -n -- "--note-1" DESIGN.md; grep -n -- "--shadow-none" DESIGN.md
```

Expected: 세 grep 모두 매치 0건 (exit 1).

```bash
grep -c -- "--surface-note-1\|--space-7\|--motion-expand\|--radius-board" DESIGN.md
```

Expected: 4 이상.

- [ ] **Step 7: Commit**

```bash
git add SKILL.md DESIGN.md
git commit -m "docs: 낡은 캐시 메모 제거, DESIGN.md 토큰 표를 템플릿 실측과 일치 (D1 문서부)"
```

---

### Task 2: .gitignore 화이트리스트 일반화 + 테스트 스크래치 예약 (D5)

**Files:**
- Modify: `.gitignore` (전체 교체)

**Interfaces:**
- Consumes: 없음
- Produces: `tests/.out/` 무시 규칙 (Task 3이 사용), `.omo/plans/*.md`·`.omo/evidence/*.md` 자동 추적 (이 계획 파일 포함), `.omo/evidence/design-next/` 리포트 화이트리스트 (Task 9가 사용).

- [ ] **Step 1: .gitignore 전체 교체**

```gitignore
# Python runtime artifacts
__pycache__/
*.py[cod]

# Test scratch output (Task 3 이후 테스트가 여기에만 씀)
tests/.out/

# SDD 실행 레저 (세션 진행 기록 — 커밋 금지)
.superpowers/

# OMO workspace artifacts: 리뷰 가능한 plan/evidence 마크다운은 추적, 생성물 벌크는 무시.
.omo/**
!.omo/
!.omo/plans/
!.omo/plans/*.md
!.omo/evidence/
!.omo/evidence/*.md
!.omo/evidence/task-8-mindmap-html-generator-design-upgrade/
!.omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs
!.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/
!.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json
!.omo/evidence/design-next/
!.omo/evidence/design-next/*.md
!.omo/evidence/design-next/browser-visual-qa-report.json
```

- [ ] **Step 2: 추적 상태 검증**

```bash
git status --short
```

Expected: 기존 추적 파일에 삭제(D) 표시가 없고, `.omo/plans/mindmap-html-generator-v3.1-refactor-and-design-next.md`가 신규(??)로 나타남. `.omo/evidence/**/out/` 생성물은 여전히 무시됨:

```bash
git check-ignore -v tests/.out/x.html .omo/evidence/readme-release/out/x.html
```

Expected: 두 경로 모두 무시 규칙 매치 출력.

- [ ] **Step 3: Commit (이 계획 파일 포함)**

```bash
git add .gitignore .omo/plans/mindmap-html-generator-v3.1-refactor-and-design-next.md
git commit -m "chore: .gitignore 화이트리스트 일반화 + v3.1 계획 문서 추가 (D5)"
```

---

### Task 3: 테스트 스크래치 경로를 evidence 밖으로 이전

**Files:**
- Modify: `tests/test_build_mindmap.py:14` 및 `EVIDENCE_OUT` 전체 참조

**Interfaces:**
- Consumes: Task 2의 `tests/.out/` 무시 규칙
- Produces: 상수 `SCRATCH_OUT: Path = REPO_ROOT / "tests" / ".out"` — 이후 모든 테스트(Task 4~7)가 이 상수를 사용.

배경: 현재 `EVIDENCE_OUT`은 `.omo/evidence/task-3-mindmap-html-generator-upgrade/out`(존재하지 않는 옛 과업명 경로)이며, 테스트 실행 시마다 증거 폴더에 생성물을 쓴다. 스크래치는 evidence와 분리한다.

- [ ] **Step 1: 상수 교체**

`tests/test_build_mindmap.py:14`의

```python
EVIDENCE_OUT = REPO_ROOT / ".omo" / "evidence" / "task-3-mindmap-html-generator-upgrade" / "out"
```

교체:

```python
SCRATCH_OUT = REPO_ROOT / "tests" / ".out"
```

파일 내 `EVIDENCE_OUT` 참조 전체(setUp 포함 10곳)를 `SCRATCH_OUT`으로 치환.

- [ ] **Step 2: 테스트 실행으로 회귀 확인**

```bash
python tests/test_build_mindmap.py
```

Expected: 9 tests, OK. `tests/.out/` 아래에만 생성물이 생김.

- [ ] **Step 3: 옛 스크래치 잔재 삭제 (캐시 생성물 — 삭제 허용 범위)**

한글 경로이므로 Python 스크립트 파일로 실행:

```python
# scratch cleanup: cleanup_old_scratch.py (스크래치 디렉터리에 저장 후 실행)
import shutil
from pathlib import Path
p = Path(r"C:/Users/홍주형/.claude/skills/mindmap-html-generator/.omo/evidence/task-3-mindmap-html-generator-upgrade")
if p.exists():
    shutil.rmtree(p)
    print("removed:", p)
else:
    print("already absent:", p)
```

Expected: `removed: ...` 또는 `already absent: ...`.

- [ ] **Step 4: git 상태 확인 후 Commit**

```bash
git status --short
git add tests/test_build_mindmap.py
git commit -m "refactor(tests): 스크래치 출력을 evidence에서 tests/.out으로 이전"
```

Expected: 커밋에 테스트 파일 1개만 포함.

---

### Task 4: 빌더 내부 구조 리팩토링 — SpecError + 순수 render_html 분리 (단일 파일 유지)

**Files:**
- Modify: `scripts/build_mindmap.py` (`build()`·`main()` 교체, `SpecError`·`render_html()` 추가)
- Test: `tests/test_build_mindmap.py` (in-process 단위 테스트 클래스 추가)

**Interfaces:**
- Consumes: Task 3의 `SCRATCH_OUT`
- Produces:
  - `class SpecError(ValueError)` — 속성 `errors: list[str]`
  - `render_html(spec: dict, template: str) -> tuple[str, dict]` — 파일 I/O 없는 순수 렌더. 반환 meta 키: `"mode": str`, `"subject": str`(폴백 시 빈 문자열), `"sides": list[str]`, `"warnings": list[str]`
  - `build(spec_path, out_dir=None, template_path=None) -> Path` — 검증 실패 시 `sys.exit` 대신 `SpecError` raise; CLI 출력(경고·완료 메시지)은 기존과 동일
  - `main()` — `SpecError`를 잡아 `[오류] ...` 출력 후 `sys.exit(1)` (CLI 동작 불변)

- [ ] **Step 1: 실패하는 단위 테스트 작성**

`tests/test_build_mindmap.py` 끝(`if __name__ == "__main__":` 앞)에 추가:

```python
import importlib.util


def _load_builder_module():
    module_spec = importlib.util.spec_from_file_location("build_mindmap", BUILDER)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


class BuilderUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bm = _load_builder_module()
        cls.template = (REPO_ROOT / "assets" / "base-mindmap-template.html").read_text(encoding="utf-8")

    def test_render_html_returns_html_and_meta_without_io(self) -> None:
        spec = {
            "title": "테스트 주제",
            "mode": "퀴즈형",
            "center": {"title": "중심", "text": "설명"},
            "branches": [{"title": "가지", "details": ["항목"]}],
        }
        html_text, meta = self.bm.render_html(spec, self.template)
        self.assertNotIn("{{", html_text)
        self.assertIn('data-mode="퀴즈형"', html_text)
        self.assertEqual(meta["mode"], "퀴즈형")
        self.assertEqual(meta["sides"], ["left"])
        self.assertEqual(meta["warnings"], ["퀴즈형 모드인데 quiz 항목이 있는 브랜치가 없음"])

    def test_render_html_unsupported_subject_falls_back_with_warning(self) -> None:
        spec = {
            "title": "테스트",
            "subject": "철학",
            "center": {"title": "중심", "text": "설명"},
            "branches": [{"title": "가지"}],
        }
        html_text, meta = self.bm.render_html(spec, self.template)
        self.assertEqual(meta["subject"], "")
        self.assertNotIn("data-subject=", html_text.splitlines()[1])
        self.assertIn("교과 '철학' 테마 미지원", meta["warnings"][0])

    def test_build_raises_spec_error_with_korean_messages(self) -> None:
        SCRATCH_OUT.mkdir(parents=True, exist_ok=True)
        bad = SCRATCH_OUT / "bad-spec.json"
        bad.write_text('{"title": "x"}', encoding="utf-8")
        with self.assertRaises(self.bm.SpecError) as ctx:
            self.bm.build(bad, SCRATCH_OUT / "bad-out")
        self.assertIn("필수 키 누락: center", ctx.exception.errors)
        self.assertIn("필수 키 누락: branches", ctx.exception.errors)
```

- [ ] **Step 2: 실패 확인**

```bash
python tests/test_build_mindmap.py
```

Expected: 신규 3개 테스트가 `AttributeError: ... has no attribute 'render_html'` / `'SpecError'`로 FAIL(ERROR), 기존 9개는 PASS.

- [ ] **Step 3: 빌더 구현**

`scripts/build_mindmap.py`에서 `def build(...)`~`def main(...)` 전체를 아래로 교체 (그 위의 헬퍼·상수·docstring은 그대로):

```python
class SpecError(ValueError):
    """스펙 검증 실패. errors에 한국어 메시지 목록을 담는다."""

    def __init__(self, errors):
        super().__init__("; ".join(errors))
        self.errors = list(errors)


def render_html(spec, template):
    """검증된 spec과 템플릿 문자열로 최종 HTML을 만든다 (파일 I/O 없음).

    반환: (html 문자열, meta dict) — meta 키: mode, subject, sides, warnings
    """
    warnings = []
    mode = spec.get("mode", "교과용")
    subject = (spec.get("subject") or "").strip()
    if subject and subject not in SUPPORTED_SUBJECTS:
        warnings.append(
            f"교과 '{subject}' 테마 미지원 — 기본 테마 적용 (지원: {', '.join(SUPPORTED_SUBJECTS)})"
        )
        subject = ""

    branches = spec["branches"]
    sides = assign_sides(branches)
    if mode == "퀴즈형" and not any(b.get("quiz") for b in branches):
        warnings.append("퀴즈형 모드인데 quiz 항목이 있는 브랜치가 없음")

    branch_html = "\n\n      ".join(
        build_branch_html(branch, i + 1, sides[i]) for i, branch in enumerate(branches)
    )
    pedagogy_html = build_pedagogy_html(spec.get("pedagogy"))

    default_hint = QUIZ_HINT if mode == "퀴즈형" else DEFAULT_HINT
    result = template
    if subject:
        result = result.replace('data-subject="{{SUBJECT}}"', f'data-subject="{esc(subject)}"')
    else:
        result = result.replace(' data-subject="{{SUBJECT}}"', "")
    result = (
        result
        .replace("{{MODE}}", esc(mode))
        .replace("{{TITLE}}", esc(spec["title"]))
        .replace("{{DESCRIPTION}}", esc(spec.get("description", "")))
        .replace("{{CENTER_TITLE}}", esc(spec["center"]["title"]))
        .replace("{{CENTER_TEXT}}", esc(spec["center"]["text"]))
        .replace("{{PEDAGOGY}}", pedagogy_html)
        .replace("{{BRANCHES}}", branch_html)
        .replace("{{HINT}}", esc(spec.get("hint", default_hint)))
    )
    return result, {"mode": mode, "subject": subject, "sides": sides, "warnings": warnings}


def build(spec_path, out_dir=None, template_path=None):
    spec_path = Path(spec_path)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    errors = validate_spec(spec)
    if errors:
        raise SpecError(errors)

    if template_path is None:
        template_path = Path(__file__).resolve().parent.parent / "assets" / "base-mindmap-template.html"
    template = Path(template_path).read_text(encoding="utf-8")

    result, meta = render_html(spec, template)
    for warning in meta["warnings"]:
        print(f"[경고] {warning}")

    out_dir = Path(out_dir) if out_dir else spec_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{sanitize_filename(spec['title'])}_{meta['mode']}.html"
    out_path.write_text(result, encoding="utf-8")

    sides = meta["sides"]
    left_count = sides.count("left")
    print(f"[완료] {out_path}")
    print(
        f"  모드: {meta['mode']} / 교과 테마: {meta['subject'] or '기본(그린)'} / "
        f"브랜치: {len(sides)}개 (좌 {left_count}·우 {len(sides) - left_count})"
    )
    return out_path


def main():
    parser = argparse.ArgumentParser(description="JSON 스펙으로 마인드맵 HTML 생성")
    parser.add_argument("spec", help="JSON 스펙 파일 경로")
    parser.add_argument("-o", "--out-dir", default=None, help="출력 폴더 (기본: 스펙 파일 위치)")
    parser.add_argument("--template", default=None, help="템플릿 경로 (기본: 스킬 내장 템플릿)")
    args = parser.parse_args()
    try:
        build(args.spec, args.out_dir, args.template)
    except SpecError as err:
        for message in err.errors:
            print(f"[오류] {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

주의: 기존 `build()` 내부의 경고 출력 순서(교과 미지원 → 퀴즈 없음)를 `warnings` append 순서로 보존했고, `[오류]`/`[경고]`/`[완료]` 문자열은 그대로다 — 기존 서브프로세스 테스트가 이를 검증한다.

- [ ] **Step 4: 전체 테스트 통과 확인**

```bash
python -m py_compile scripts/build_mindmap.py
python tests/test_build_mindmap.py
```

Expected: 12 tests, OK (기존 9 + 신규 3).

- [ ] **Step 5: Commit**

```bash
git add scripts/build_mindmap.py tests/test_build_mindmap.py
git commit -m "refactor(builder): SpecError와 순수 render_html 분리, CLI 동작 불변"
```

---

### Task 5: D4 — 부분 pedagogy fixture와 빈 라벨 방지 검증

**Files:**
- Create: `tests/fixtures/pedagogy-single-field.json`
- Test: `tests/test_build_mindmap.py` (`BuildMindmapCompatibilityTests`에 메서드 추가)

**Interfaces:**
- Consumes: `run_builder(fixture_name, out_dir)`, `SCRATCH_OUT`
- Produces: pedagogy 1필드 fixture — D4의 "no / one-field / full" 3종 매트릭스 완성 (no=`current-v2-valid.json`, full=`v3-pedagogy.json` 기존 존재).

- [ ] **Step 1: fixture 작성**

`tests/fixtures/pedagogy-single-field.json` (UTF-8):

```json
{
  "title": "분수의 덧셈",
  "description": "분모가 같은 분수의 덧셈 정리",
  "subject": "수학",
  "center": {"title": "분수의 덧셈", "text": "분모가 같을 때"},
  "branches": [
    {"title": "개념", "details": ["분모는 그대로 두고 분자끼리 더한다"]},
    {"title": "예시", "details": ["1/5 + 2/5 = 3/5"]}
  ],
  "pedagogy": {"focus_question": "왜 분모는 더하지 않을까?"}
}
```

- [ ] **Step 2: 실패하는 테스트 작성**

```python
    def test_single_field_pedagogy_renders_only_that_item(self) -> None:
        out_dir = SCRATCH_OUT / "pedagogy-single-field"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("pedagogy-single-field.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html = (out_dir / "분수의_덧셈_교과용.html").read_text(encoding="utf-8")
        self.assertIn('<aside class="pedagogy" aria-label="학습 지원 정보">', html)
        self.assertEqual(html.count('<li class="pedagogy-item">'), 1)
        self.assertIn("초점 질문", html)
        for absent_label in ("학년군", "선수 지식", "오개념 점검", "어휘 지원", "형성 확인 유형"):
            self.assertNotIn(absent_label, html)
        self.assertNotIn("{{", html)
```

- [ ] **Step 3: 실행 — fixture 없으면 FAIL, 있으면 PASS 확인**

```bash
python tests/test_build_mindmap.py
```

Expected: fixture 작성 후이므로 13 tests, OK. (fixture를 Step 1에서 이미 만들었으므로 이 테스트는 렌더러가 이미 D4 규칙을 지키는지 확인하는 회귀 고정 테스트다. FAIL이 나오면 `build_pedagogy_html`의 빈 라벨 처리 버그이므로 수정 후 재실행.)

- [ ] **Step 4: Commit**

```bash
git add tests/fixtures/pedagogy-single-field.json tests/test_build_mindmap.py
git commit -m "test: D4 부분 pedagogy fixture — 값 있는 항목만 렌더링 검증"
```

---

### Task 6: D2 — 장문 한글 제목·어휘 중심 fixture

**Files:**
- Create: `tests/fixtures/design-long-title.json`
- Create: `tests/fixtures/design-vocab-heavy.json`
- Test: `tests/test_build_mindmap.py`

**Interfaces:**
- Consumes: `run_builder`, `SCRATCH_OUT`
- Produces: Task 9 브라우저 QA가 사용할 D2 스트레스 샘플 2종. 산출 파일명: `일제강점기_국내외_민족_운동의_전개와_국제_정세_변화_교과용.html`, `물질의_상태_변화_어휘_정리_교과용.html`.

- [ ] **Step 1: 장문 제목 fixture 작성**

`tests/fixtures/design-long-title.json` (UTF-8):

```json
{
  "title": "일제강점기 국내외 민족 운동의 전개와 국제 정세 변화",
  "description": "장문 제목·장문 브랜치 라벨에서 한글 줄바꿈과 위계가 유지되는지 검증하는 D2 fixture",
  "subject": "역사",
  "center": {"title": "일제강점기 민족 운동", "text": "국내외 전개 양상과 국제 정세의 상호작용"},
  "branches": [
    {"title": "1910년대 국내 비밀 결사와 국외 독립운동 기지 건설", "details": ["독립의군부·대한광복회 활동", "만주·연해주 독립운동 기지 건설 노력"]},
    {"title": "3·1 운동의 전개 과정과 국내외 파급 효과", "details": ["민족 자결주의와 2·8 독립 선언의 영향", "대한민국 임시 정부 수립으로 이어진 흐름"]},
    {"title": "1920년대 실력 양성 운동과 대중 운동의 확산", "details": ["물산 장려 운동과 민립 대학 설립 운동", "소년·형평·여성 운동 등 대중 운동의 성장"]},
    {"title": "1930년대 이후 무장 투쟁과 건국 준비 활동", "details": ["한중 연합 작전과 조선 의용대·한국광복군", "건국 강령 발표와 광복 준비"]}
  ],
  "pedagogy": {
    "grade_band": "middle 3",
    "focus_question": "국제 정세 변화는 민족 운동의 방식과 방향을 어떻게 바꾸었을까?",
    "lesson_purpose": "정리"
  }
}
```

- [ ] **Step 2: 어휘 중심 fixture 작성**

`tests/fixtures/design-vocab-heavy.json` (UTF-8):

```json
{
  "title": "물질의 상태 변화 어휘 정리",
  "description": "과학 핵심 어휘가 밀집된 상황의 가독성을 검증하는 D2 fixture",
  "subject": "과학",
  "center": {"title": "상태 변화", "text": "입자 배열과 에너지 출입"},
  "branches": [
    {"title": "융해·응고", "details": ["융해: 고체 → 액체, 열에너지 흡수", "응고: 액체 → 고체, 열에너지 방출", "융해열·응고열은 크기가 같다"]},
    {"title": "기화·액화", "details": ["기화: 증발과 끓음으로 구분", "액화: 기체 → 액체, 열에너지 방출", "끓는점은 압력에 따라 달라진다"]},
    {"title": "승화", "details": ["고체 ↔ 기체 직접 변화", "드라이아이스·아이오딘·성에가 대표 사례"]},
    {"title": "입자 모형", "details": ["상태 변화 전후 입자의 종류·개수·질량 불변", "입자 배열과 입자 사이 거리만 변한다"]}
  ],
  "pedagogy": {
    "grade_band": "middle 1",
    "lesson_purpose": "복습",
    "vocabulary_support": ["융해", "응고", "기화", "액화", "승화", "증발", "끓는점", "열에너지"],
    "misconceptions": ["상태가 변하면 입자 자체가 변한다는 오개념", "증발은 끓는점에서만 일어난다는 오개념"]
  }
}
```

- [ ] **Step 3: 실패하는 테스트 작성 후 실행**

```python
    def test_design_long_title_fixture_builds_clean(self) -> None:
        out_dir = SCRATCH_OUT / "design-long-title"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("design-long-title.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html = (out_dir / "일제강점기_국내외_민족_운동의_전개와_국제_정세_변화_교과용.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('<div class="node branch-'), 4)
        self.assertIn('data-subject="역사"', html)
        self.assertNotIn("{{", html)

    def test_design_vocab_heavy_fixture_builds_clean(self) -> None:
        out_dir = SCRATCH_OUT / "design-vocab-heavy"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("design-vocab-heavy.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html = (out_dir / "물질의_상태_변화_어휘_정리_교과용.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('<div class="node branch-'), 4)
        self.assertIn("어휘 지원", html)
        self.assertIn("오개념 점검", html)
        self.assertNotIn("{{", html)
```

```bash
python tests/test_build_mindmap.py
```

Expected: 15 tests, OK.

- [ ] **Step 4: Commit**

```bash
git add tests/fixtures/design-long-title.json tests/fixtures/design-vocab-heavy.json tests/test_build_mindmap.py
git commit -m "test: D2 장문 제목·어휘 중심 fixture 추가"
```

---

### Task 7: D3 — 전 상태 showcase fixture

**Files:**
- Create: `tests/fixtures/design-state-showcase.json`
- Test: `tests/test_build_mindmap.py`

**Interfaces:**
- Consumes: `run_builder`, `SCRATCH_OUT`
- Produces: 브랜치 8개(최대치)·퀴즈 2개·pedagogy 포함 단일 showcase — Task 9의 브라우저 QA가 collapsed/expanded/hover/focus/active/quiz open·closed/print 상태를 이 한 파일로 구동. 산출 파일명: `상태_점검_쇼케이스_퀴즈형.html`.

- [ ] **Step 1: fixture 작성**

`tests/fixtures/design-state-showcase.json` (UTF-8). 퀴즈 키는 저장소 내부 QA 목적 사용(승인 규칙의 기존 `quiz-approved.json` 선례를 따름):

```json
{
  "title": "상태 점검 쇼케이스",
  "description": "브랜치 8개·퀴즈·학습 지원 패널의 모든 상호작용 상태를 한 파일로 점검하는 QA 전용 fixture",
  "subject": "정보",
  "mode": "퀴즈형",
  "center": {"title": "상태 쇼케이스", "text": "collapsed·expanded·hover·focus·quiz·print"},
  "branches": [
    {"title": "정의", "sub": "짧은 부제", "icon": "bi-book", "details": ["기본 브랜치 상태 점검용 불릿"]},
    {"title": "분류", "details": ["두 번째 브랜치", "불릿 두 줄 케이스"]},
    {"title": "규칙", "details": ["세 번째 브랜치"]},
    {"title": "예시", "details": ["네 번째 브랜치"], "quiz": {"q": "이 브랜치의 상태는 무엇으로 점검하나요?", "a": "정답 보기 버튼의 열림·닫힘 상태로 점검합니다."}},
    {"title": "한계", "details": ["다섯 번째 브랜치"]},
    {"title": "적용", "details": ["여섯 번째 브랜치"], "quiz": {"q": "퀴즈 두 번째 상태 점검 질문은?", "a": "두 번째 정답 텍스트입니다."}},
    {"title": "비교", "details": ["일곱 번째 브랜치"]},
    {"title": "정리", "details": ["여덟 번째 브랜치 — 최대치 확인"]}
  ],
  "pedagogy": {
    "focus_question": "모든 상태가 시각적으로 구분되는가?",
    "lesson_purpose": "평가",
    "assessment_prompt_types": ["explanation", "misconception check"]
  }
}
```

- [ ] **Step 2: 실패하는 테스트 작성 후 실행**

```python
    def test_design_state_showcase_covers_max_branches_and_quiz(self) -> None:
        out_dir = SCRATCH_OUT / "design-state-showcase"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("design-state-showcase.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html = (out_dir / "상태_점검_쇼케이스_퀴즈형.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('<div class="node branch-'), 8)
        self.assertEqual(html.count('<div class="quiz">'), 2)
        self.assertIn('<aside class="pedagogy"', html)
        self.assertIn('data-mode="퀴즈형"', html)
        self.assertNotIn("{{", html)
```

```bash
python tests/test_build_mindmap.py
```

Expected: 16 tests, OK.

- [ ] **Step 3: Commit**

```bash
git add tests/fixtures/design-state-showcase.json tests/test_build_mindmap.py
git commit -m "test: D3 전 상태 showcase fixture (브랜치 8·퀴즈 2·pedagogy)"
```

---

### Task 8: 스큐어모피즘 + 전 테마 멀티 컬러 노트 (사용자 승인된 디자인 진화)

**Files:**
- Modify: `DESIGN.md` (§1 Atmosphere, §2 Color, §7 Depth — 계약 먼저)
- Modify: `SKILL.md` (디자인 계약 문단 한 줄 추가)
- Modify: `assets/base-mindmap-template.html` (토큰·노드·테마 블록)
- Test: `tests/test_build_mindmap.py` (`TemplateContractTests` 클래스 추가)

**Interfaces:**
- Consumes: Task 1이 정렬한 `DESIGN.md` 토큰 표, Task 3의 `SCRATCH_OUT`(간접)
- Produces: 신규 토큰 `--shadow-note-rest`, `--shadow-note-raised`, `--shadow-note-pressed`, `--paper-sheen`, `--surface-tape`, `--border-tape`, `--surface-frame`, `--border-frame`; 전 테마 8색(6계열 이상) 노트 상속 구조 — Task 9 브라우저 QA가 이 상태를 검증.

설계 결정 (실측 근거):

- **멀티 컬러**: 현재 13개 `[data-subject]` 테마 블록이 `--card1`~`--card8`을 단색조 틴트로 덮어써 테마 적용 시 노트가 사실상 1색이 된다. 기본 `:root`의 `--card1~8`은 이미 핑크·주황·노랑·초록·청록·파랑·보라·자주 8계열이므로, **테마 블록에서 `--card` 재정의를 전부 제거**해 전 테마가 기본 8색을 상속하게 한다. 교과 정체성은 `--bg`·`--center1/2`·`--line`으로 유지된다.
- **스큐어모피즘 제약**: `.node`가 `overflow: hidden`이라 테이프 요소가 잘린다 → `overflow: visible`로 바꾸고 버튼에 radius 보상을 준다. 회전은 절대 배치 레이아웃인 `@media (min-width: 1201px)`에만 적용한다(±0.5deg 이하 — 연결선 오차 1px 내). 인쇄는 전부 평면화.

- [ ] **Step 1: DESIGN.md·SKILL.md 계약 갱신 (템플릿 수정 전 필수)**

`DESIGN.md` §1 Atmosphere 끝에 추가:

```markdown
The workspace is rendered with restrained skeuomorphism: branch notes read as real paper sticky notes (paper sheen, layered contact shadows, translucent tape, a slight resting tilt on desktop), and the board reads as a physical whiteboard with a light frame. Skeuomorphic cues are texture-free CSS only, must never reduce Korean text contrast, and must flatten in print.
```

`DESIGN.md` §2 Palette 표에 행 추가:

```markdown
| Tape | `--surface-tape` / `--border-tape` | translucent white | Sticky-note tape accent |
| Frame | `--surface-frame` / `--border-frame` | light warm gray | Whiteboard frame around the map |
| Sheen | `--paper-sheen` | white-fade linear gradient | Paper top-light on branch notes |
```

`DESIGN.md` §2 Rules에 추가:

```markdown
- Branch note surfaces must span at least 6 distinct hue families in every subject theme. Subject identity lives in the canvas tint, center node, and connectors (legacy override surface `--bg`, `--center1/2`, `--line`) — never by collapsing note colors into a single hue.
```

`DESIGN.md` §7 Depth 표에 행 추가 + Rules에 한 줄 추가:

```markdown
| Note rest | `--shadow-note-rest` | Sticky notes at rest (contact + ambient + inner top light) |
| Note raised | `--shadow-note-raised` | Hover/expanded "picked up" state |
| Note pressed | `--shadow-note-pressed` | Button pressed inset |
```

```markdown
- Paper-stack shadows, tape, and a light board frame are the default skeuomorphic depth. No glossy bevels, linen textures, or heavy 2010s-iOS gloss.
```

`SKILL.md` "디자인 계약" 문단 끝에 추가:

```markdown
v3.1부터 절제된 스큐어모피즘(종이 질감 스티키 노트·테이프·화이트보드 프레임·데스크톱 미세 기울기)과
전 교과 테마 6색 이상 노트 팔레트가 기본이다. 스큐어모피즘 큐는 CSS 전용이며 인쇄 시 평면화된다.
```

- [ ] **Step 2: 실패하는 템플릿 계약 테스트 작성**

`tests/test_build_mindmap.py`에 클래스 추가 (`if __name__ == "__main__":` 앞):

```python
class TemplateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template = (REPO_ROOT / "assets" / "base-mindmap-template.html").read_text(encoding="utf-8")

    def test_subject_themes_inherit_multi_hue_note_palette(self) -> None:
        # --cardN 정의는 :root 1곳뿐이어야 함 — 테마 블록이 단색조로 덮어쓰면 실패
        for n in range(1, 9):
            self.assertEqual(
                self.template.count(f"--card{n}:"), 1,
                f"--card{n} 재정의 발견 — 테마 블록은 기본 8색 팔레트를 상속해야 함",
            )

    def test_template_declares_skeuomorph_tokens_and_print_flatten(self) -> None:
        for token in ("--shadow-note-rest", "--shadow-note-raised", "--shadow-note-pressed",
                      "--paper-sheen", "--surface-tape", "--surface-frame"):
            self.assertIn(token, self.template)
        self.assertIn(".node:not(.center)::after", self.template)
```

```bash
python tests/test_build_mindmap.py
```

Expected: 신규 2개 FAIL (`--card1:` count 14 ≠ 1 / 토큰 미존재), 기존 16개 PASS.

- [ ] **Step 3: 템플릿 `:root`에 스큐어모피즘 토큰 추가**

`--motion-control` 선언 다음 줄에 추가:

```css
      --shadow-note-rest: 0 1px 2px rgba(56, 72, 66, 0.10), 0 10px 18px rgba(56, 72, 66, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.65);
      --shadow-note-raised: 0 2px 4px rgba(56, 72, 66, 0.12), 0 18px 30px rgba(56, 72, 66, 0.17), inset 0 1px 0 rgba(255, 255, 255, 0.65);
      --shadow-note-pressed: inset 0 2px 5px rgba(56, 72, 66, 0.16);
      --paper-sheen: linear-gradient(180deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0) 46%);
      --surface-tape: rgba(255, 255, 255, 0.5);
      --border-tape: rgba(255, 255, 255, 0.68);
      --surface-frame: #eef1ef;
      --border-frame: rgba(92, 109, 102, 0.28);
```

- [ ] **Step 4: 노드를 스티키 노트로 — overflow 전환 + 테이프 + 눌림 상태**

`.node` 블록(168행 부근)에서 `overflow: hidden;` → `overflow: visible;`, `box-shadow: var(--shadow-rest);` → `box-shadow: var(--shadow-note-rest);`로 바꾸고 `background` 아래에 `background-image: var(--paper-sheen);` 추가.

`.node:not(.center):hover, .node.active` 블록의 `box-shadow: var(--shadow-focus);` → `box-shadow: var(--shadow-note-raised);`.

overflow 전환 보상 — `.node > button` 블록에 추가:

```css
    .node > button {
      border-radius: calc(var(--radius-node) - 1px);
    }

    .node.active > button {
      border-radius: calc(var(--radius-node) - 1px) calc(var(--radius-node) - 1px) 0 0;
    }
```

(기존 `.node > button` 선언에 radius 속성만 병합해도 됨. `.node > button:active`에는 `box-shadow: var(--shadow-note-pressed);` 추가.)

테이프 pseudo-element (`.branch-8 { ... }` 다음에 추가):

```css
    .node:not(.center)::after {
      content: "";
      position: absolute;
      top: -9px;
      left: 50%;
      width: 76px;
      height: 22px;
      transform: translateX(-50%) rotate(-2.5deg);
      background: var(--surface-tape);
      border: 1px solid var(--border-tape);
      border-radius: 2px;
      box-shadow: 0 1px 2px rgba(56, 72, 66, 0.12);
      pointer-events: none;
      z-index: 2;
    }
```

화이트보드 프레임 — `.map` 블록에 추가:

```css
      border: 10px solid var(--surface-frame);
      outline: 1px solid var(--border-frame);
```

센터 노드 엠보스 강화 — `.center`의 box-shadow를 다음으로 교체:

```css
      box-shadow: var(--shadow-focus), inset 0 2px 0 rgba(255, 255, 255, 0.4), inset 0 -12px 26px rgba(36, 50, 45, 0.16);
```

- [ ] **Step 5: 데스크톱 전용 미세 기울기**

`@media (min-width: 1201px)` 블록(512행 부근) 안에 추가 (연결선 오차 ≤1px 유지 위해 ±0.5deg 이하):

```css
      .node:not(.center) { transform: rotate(-0.45deg); }
      .node.branch-2, .node.branch-5, .node.branch-8 { transform: rotate(0.5deg); }
      .node.branch-3, .node.branch-6 { transform: rotate(-0.2deg); }
      .node:not(.center):hover, .node.active { transform: rotate(0deg); }
```

- [ ] **Step 6: 테마 블록의 `--card1`~`--card8` 재정의 전부 제거**

13개 `[data-subject="..."]` 블록에서 `--card1:`~`--card8:` 선언 줄만 삭제 (`--bg`·`--center1`·`--center2`·`--line`은 유지). 삭제 후 각 테마는 `:root`의 8색 팔레트를 상속한다.

- [ ] **Step 7: 인쇄 평면화**

`@media print` 블록(647행 부근)에 추가:

```css
      .node:not(.center)::after { display: none; }
      .node { transform: none; box-shadow: none; background-image: none; }
      .map { border: 1px solid var(--border-subtle); outline: none; }
```

- [ ] **Step 8: 테스트 통과 + 회귀 확인**

```bash
python tests/test_build_mindmap.py
```

Expected: 18 tests, OK (기존 16 + 신규 2).

```bash
grep -c -- "--card1:" assets/base-mindmap-template.html
```

Expected: 1.

- [ ] **Step 9: Commit**

```bash
git add DESIGN.md SKILL.md assets/base-mindmap-template.html tests/test_build_mindmap.py
git commit -m "feat(design): 절제된 스큐어모피즘 + 전 테마 멀티 컬러 노트 팔레트 (v3.1)"
```

---

### Task 9: visual QA 스크립트 승격 + 브라우저 QA 실행 (D1~D4 + 스큐어모피즘 시각 검증)

**Files:**
- Move: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs` → `tests/visual-qa.mjs`
- Modify: `tests/visual-qa.mjs` (기본 경로 상수·usage 문자열)
- Modify: `.gitignore` (옛 위치 화이트리스트 정리)
- Create(생성물): `.omo/evidence/design-next/browser-visual-qa-report.json` + 스크린샷(무시됨)

**Interfaces:**
- Consumes: Task 6·7 fixture, Task 8이 반영된 `assets/base-mindmap-template.html`, `scripts/build_mindmap.py`
- Produces: 정식 QA 진입점 `node tests/visual-qa.mjs --sample-dir .omo/evidence/design-next/out` — Task 10의 README 릴리스 체크가 이 명령을 기재.

**전제:** Playwright는 기존 설치본만 사용. `node -e "import('playwright')"`가 실패하면 이 Task를 중단하고 "렌더링 미검증"으로 보고 (임의 설치 금지).

- [ ] **Step 1: 스크립트 이동**

```bash
git mv .omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs tests/visual-qa.mjs
```

- [ ] **Step 2: 기본 경로 상수 갱신**

`tests/visual-qa.mjs` 상단:

```js
const DEFAULT_EVIDENCE_DIR = ".omo/evidence/design-next";
const DEFAULT_OUT_DIR = `${DEFAULT_EVIDENCE_DIR}/screenshots`;
```

USAGE 문자열의 `node .omo/evidence/task-8-.../visual-qa.mjs` 3곳을 `node tests/visual-qa.mjs`로, `--sample-dir` 예시 경로를 `.omo/evidence/design-next/out`으로 교체.

- [ ] **Step 3: .gitignore에서 옛 스크립트 화이트리스트 제거**

Task 2 결과물에서 아래 한 줄 삭제 (스크린샷 리포트 화이트리스트는 과거 증거로 유지):

```
!.omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs
```

- [ ] **Step 4: QA 샘플 4종 생성**

```bash
python scripts/build_mindmap.py tests/fixtures/current-v2-valid.json -o .omo/evidence/design-next/out
python scripts/build_mindmap.py tests/fixtures/design-long-title.json -o .omo/evidence/design-next/out
python scripts/build_mindmap.py tests/fixtures/design-vocab-heavy.json -o .omo/evidence/design-next/out
python scripts/build_mindmap.py tests/fixtures/design-state-showcase.json -o .omo/evidence/design-next/out
```

Expected: 각 명령 `[완료]` 출력, HTML 4개 생성.

- [ ] **Step 5: 브라우저 QA 실행**

```bash
node tests/visual-qa.mjs --sample-dir .omo/evidence/design-next/out
```

Expected: `browser-visual-qa-report.json` 생성, 실패 항목 0. 실패(빈 컨트롤, 보이지 않는 focus, 잘린 정답, `{{` 잔존, 가로 넘침)가 있으면 템플릿을 `DESIGN.md` 토큰 범위 안에서 수정하고 Step 4부터 재실행.

- [ ] **Step 6: 수동 검수 (Review Gate)**

데스크톱 1280px 1장, 모바일 390px 1장, 퀴즈 열림 1장, print 1장을 직접 열어 확인하고 확인 결과를 `.omo/evidence/design-next/manual-inspection.md`에 4줄로 기록:

```markdown
# design-next 수동 검수
- 데스크톱 1280px: (파일명) — 겹침/잘림 없음, 테이프·미세 기울기·화이트보드 프레임 렌더링, 노트 8색(6계열 이상) 구분 확인
- 모바일 390px: (파일명) — 세로 스택·가로 스크롤 없음, 기울기 미적용 확인
- 퀴즈 열림: (파일명) — 정답 텍스트 노출·대비 확인
- print: (파일명) — 전체 펼침·컨트롤 숨김·스큐어모피즘 평면화(테이프/기울기/그림자 제거) 확인
- 교과 테마 1종(예: 수학): (파일명) — 노트가 단색조로 무너지지 않고 멀티 컬러 유지 확인
```

- [ ] **Step 7: Commit**

```bash
git add tests/visual-qa.mjs .gitignore .omo/evidence/design-next/browser-visual-qa-report.json .omo/evidence/design-next/manual-inspection.md
git commit -m "feat(qa): visual QA 스크립트를 tests/로 승격, design-next 샘플 4종 브라우저 검증"
```

---

### Task 10: 릴리스 게이트 — README 최신화 + 전체 검증

**Files:**
- Modify: `README.md` (저장소 구조 트리, 릴리스 체크, 버전 이력)

**Interfaces:**
- Consumes: Task 1~9 전체 결과
- Produces: v3.1 릴리스 상태의 저장소 (push·Codex 동기화는 사용자 명시 요청 대기)

- [ ] **Step 1: README 저장소 구조 트리 갱신**

`tests/` 블록을 아래로 교체:

```
tests/
  test_build_mindmap.py       ← [검증] stdlib 기반 빌더 회귀 테스트 (E2E + in-process)
  visual-qa.mjs               ← [검증] Playwright 브라우저 visual QA (기존 설치본 필요)
  .out/                       ← 테스트 스크래치 (gitignore, 커밋 금지)
  fixtures/                   ← [검증] v2/v3/오류/퀴즈/디자인 QA fixture
```

- [ ] **Step 2: README 릴리스 체크 명령 갱신**

기존 릴리스 체크 코드 블록을 교체:

```powershell
python -m py_compile scripts/build_mindmap.py
python tests/test_build_mindmap.py
python scripts/build_mindmap.py tests/fixtures/current-v2-valid.json -o .omo/evidence/design-next/out
python scripts/build_mindmap.py tests/fixtures/design-long-title.json -o .omo/evidence/design-next/out
python scripts/build_mindmap.py tests/fixtures/design-vocab-heavy.json -o .omo/evidence/design-next/out
python scripts/build_mindmap.py tests/fixtures/design-state-showcase.json -o .omo/evidence/design-next/out
node tests/visual-qa.mjs --sample-dir .omo/evidence/design-next/out
```

- [ ] **Step 3: README 버전 이력에 v3.1 추가**

```markdown
- **v3.1** — 절제된 스큐어모피즘(스티키 노트·테이프·화이트보드 프레임·데스크톱 미세 기울기) + 전 교과 테마 6색 이상 노트 팔레트, 빌더 내부 리팩토링(SpecError·순수 render_html), 테스트 스크래치 분리, D1 토큰 계약 실측 정렬, D2~D4 fixture(장문 제목·어휘 중심·부분 pedagogy·상태 showcase), visual QA 스크립트 tests/ 승격, .gitignore 일반화
```

- [ ] **Step 4: 최종 전체 검증**

```bash
python -m py_compile scripts/build_mindmap.py
python tests/test_build_mindmap.py
git diff --check
git status --short
```

Expected: 18 tests OK, diff-check 통과(줄바꿈 경고 외 없음), 미추적 생성물은 gitignore로 모두 무시 상태.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: README v3.1 — 구조 트리·릴리스 체크·버전 이력 갱신"
```

- [ ] **Step 6: 종료 보고**

사용자에게 커밋 목록을 제시하고 push 여부·Codex 동기화 여부를 확인받는다 (자동 실행 금지).

---

## 계획 밖 (Non-Goals — design-next에서 승계)

- 수업안·학습지·판서안·평가기준표 생성기로의 확장 금지.
- 자동 퀴즈·타이머·점수·드래그·물리·staged reveal·autoplay 추가 금지 (명시 승인 전).
- 브랜드 팔레트·로고·제품 chrome 복제 금지.
- 생성 HTML·스크린샷 PNG 기본 커밋 금지.
- 레거시 별칭 토큰(`--bg`·`--card`·`--line` 등) 전면 개명·제거 — 테마 오버라이드 표면이므로 시각 회귀 리스크 대비 이득이 없어 제외. Task 8의 스큐어모피즘·멀티 컬러 변경은 이 별칭 구조 위에 추가하는 방식이며 별칭 자체는 건드리지 않는다.
- 과도한 스큐어모피즘(글로시 베벨, linen 텍스처, 외부 텍스처 이미지, 무거운 3D) 금지 — 절제된 종이 은유까지만.
