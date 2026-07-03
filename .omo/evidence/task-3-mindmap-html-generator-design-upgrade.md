# Task 3 Evidence: normalize template tokens against DESIGN.md

Timestamp: 2026-07-03T12:55:00+09:00

Verdict: complete

## Artifacts

- `assets/base-mindmap-template.html`
- `.omo/evidence/task-3-mindmap-html-generator-design-upgrade/out/기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
- `.omo/evidence/task-3-mindmap-html-generator-design-upgrade/out/알고리즘_사고_점검_마인드맵_퀴즈형.html`

## What changed

The template now exposes semantic token families that trace back to `DESIGN.md`:

- Surface tokens: `--surface-canvas`, `--surface-board`, `--surface-panel`, `--surface-note-1` through `--surface-note-8`
- Text and border tokens: `--text-primary`, `--text-secondary`, `--border-subtle`, `--border-on-note`
- Interaction and structure tokens: `--focus-ring`, `--radius-*`, `--space-*`, `--shadow-*`, `--motion-expand`

Existing theme variables remain as compatibility aliases so the generated HTML stays single-file and dependency-free.

## Commands

- `grep -n -- '--space-\|--radius-\|--surface-\|--text-\|--border-\|--focus-\|--motion-' assets/base-mindmap-template.html`
  - Exit: 0
  - Result: documented token families are present in the template and used by core map, node, quiz, and support-panel styles.
- `grep -E '#ffd02f|#0f62fe|#0066cc|#ff385c|#f54e00|#00d992' assets/base-mindmap-template.html`
  - Exit: 1
  - Result: no exact reference-brand default colors are present.
- `python -m py_compile scripts/build_mindmap.py`
  - Exit: 0
- `python tests/test_build_mindmap.py`
  - Exit: 0
  - Result: 9 regression tests passed.
- `python scripts/build_mindmap.py tests/fixtures/design-dense-korean.json -o .omo/evidence/task-3-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
- `python scripts/build_mindmap.py tests/fixtures/design-v3-pedagogy.json -o .omo/evidence/task-3-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `알고리즘_사고_점검_마인드맵_퀴즈형.html`
- `grep -R -En -- '--space-|--radius-|--surface-|data-subject|data-mode' .omo/evidence/task-3-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Result: generated HTML contains token families plus `data-subject` and `data-mode`.
- `grep -R -En '#ffd02f|#0f62fe|#0066cc|#ff385c|#f54e00|TODO|{{[^}]+}}' .omo/evidence/task-3-mindmap-html-generator-design-upgrade/out`
  - Exit: 1
  - Result: generated output has no brand-color leakage, TODO markers, or unresolved placeholders.
- `grep -En '#ffd02f|#0f62fe|#0066cc|#ff385c|#f54e00|TODO' assets/base-mindmap-template.html`
  - Exit: 1
  - Result: template has no forbidden brand-color defaults or TODO markers.
- `grep -En '{{[^}]+}}' assets/base-mindmap-template.html`
  - Exit: 0
  - Result: intentional builder placeholders remain only at template contract positions: HTML data attributes, title, description, pedagogy block, center content, branch list, and hint.
- `awk '!/^[[:space:]]*$/ && !/^[[:space:]]*(\/\/|#|--)/' assets/base-mindmap-template.html | wc -l`
  - Result: 524 nonblank/non-comment lines.
  - Classification: accepted known debt for the existing standalone generated HTML template; Todo 3 is token normalization, not a split into partials or a framework migration.
- `find . -type d -name __pycache__ -print`
  - Exit: 0 with no output after cleanup.

## Failure Scenario

The broad failure grep across both generated output and the raw template initially matched only the template's intentional `{{...}}` builder placeholders. The generated-output-only grep returned exit 1, confirming placeholders do not leak to produced HTML. Template placeholders are classified as the existing builder contract, not unfinished UI.

## Adversarial QA

- `stale_state`: dense and v3 pedagogy outputs were regenerated from the current builder and current template.
- `dirty_worktree`: token changes are in `assets/base-mindmap-template.html`; generated HTML remains under `.omo/evidence`.
- `misleading_success_output`: completion is based on source token grep, generated-output grep, negative brand/placeholder checks, compile, and tests.
- `generated_artifacts`: generated HTML is retained only under `.omo/evidence/task-3.../out`.
- `hung_or_long_commands`: all verification commands completed within bounded tool timeouts.

Cleanup: removed `scripts/__pycache__`; no server or browser session was started.
