# Task 2 Evidence: design QA fixtures and evidence harness

Timestamp: 2026-07-03T12:35:00+09:00

Verdict: complete

## Artifacts

- `tests/fixtures/design-dense-korean.json`
- `tests/fixtures/design-v3-pedagogy.json`
- `tests/fixtures/design-invalid-too-many-branches.json`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs`
- `.omo/evidence/task-2-mindmap-html-generator-design-upgrade/out/`

## Commands

- `python scripts/build_mindmap.py tests/fixtures/design-dense-korean.json -o .omo/evidence/task-2-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
  - Result: `발표용`, `사회`, 8 branches.
- `python scripts/build_mindmap.py tests/fixtures/design-v3-pedagogy.json -o .omo/evidence/task-2-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `알고리즘_사고_점검_마인드맵_퀴즈형.html`
  - Result: `퀴즈형`, `정보`, 4 branches, v3 pedagogy metadata, one approved quiz block.
- `python scripts/build_mindmap.py tests/fixtures/design-invalid-too-many-branches.json -o .omo/evidence/task-2-mindmap-html-generator-design-upgrade/out`
  - Exit: 1
  - Expected error: `[오류] 브랜치 9개 — 최대 8개 (인접 항목을 통합할 것)`.
- `node .omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs --help`
  - Exit: 0
  - Result: documented usage prints without browser launch.
- `python tests/test_build_mindmap.py`
  - Exit: 0
  - Result: 9 regression tests passed.
- `grep -R -En "data-mode|data-subject|node|초점|오개념|어휘|전이|정답 보기|{{" .omo/evidence/task-2-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Result: generated files contain data attributes, node markup, v3 pedagogy labels, and quiz reveal markers.
- `grep -R -En "{{[^}]+}}" .omo/evidence/task-2-mindmap-html-generator-design-upgrade/out`
  - Exit: 1
  - Result: no unresolved placeholders.
- `awk '!/^[[:space:]]*$/ && !/^[[:space:]]*(\/\/|#|--)/' .omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs | wc -l`
  - Result: 44 pure LOC.
- `find . -type d -name __pycache__ -print`
  - Exit: 0 with no output.

## Failure Scenario

The visual QA harness was temporarily renamed to `visual-qa.mjs.tmp`, then `node .omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs --help` exited 1 with `MODULE_NOT_FOUND`. The harness was restored and the same `--help` command exited 0.

## Coverage Notes

- `design-dense-korean.json` covers dense Korean text, long title/branch copy, 8 branches, and `발표용`.
- `design-v3-pedagogy.json` covers `퀴즈형`, v3 pedagogy metadata, quiz answer reveal, and information subject theme.
- `design-invalid-too-many-branches.json` confirms the max-eight rule remains enforced.
- Existing fixtures continue to cover `교과용` and v2 compatibility.

## Adversarial QA

- `malformed_input`: invalid 9-branch fixture fails with the expected Korean error.
- `stale_state`: outputs were regenerated from the current builder and current fixtures.
- `dirty_worktree`: generated outputs remain under `.omo/evidence`; source fixtures are intentional.
- `misleading_success_output`: build success was paired with generated-output grep checks and negative placeholder grep.
- `generated_artifacts`: generated HTML is evidence-only under `.omo/evidence/task-2.../out`.

Cleanup: no `__pycache__`, no server, no browser session.
