# Task 4 Evidence: redesign map composition and semantic structure

Timestamp: 2026-07-03T13:25:00+09:00

Verdict: complete

## Artifacts

- `DESIGN.md`
- `assets/base-mindmap-template.html`
- `.omo/evidence/task-4-mindmap-html-generator-design-upgrade/out/기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
- `.omo/evidence/task-4-mindmap-html-generator-design-upgrade/out/물의_순환_교과용.html`
- `.omo/evidence/task-4-mindmap-html-generator-design-upgrade/out/알고리즘_사고_점검_마인드맵_퀴즈형.html`

## What changed

- Added `--surface-wash` and `--surface-guide` to `DESIGN.md` and the template so the quieter page wash and board guide lines are documented tokens.
- Replaced the previous decorative radial page background with a tokenized whiteboard wash.
- Added a content-first `<header class="page-head">` around mode, title, and description.
- Changed the map section from a generic `aria-label` to a labelled region with `aria-labelledby="map-region-title"` and a screen-reader-only heading.
- Kept connector SVG decorative with `aria-hidden="true"` and added `vector-effect="non-scaling-stroke"` to generated connector paths for more stable line rendering.
- Tightened the optional pedagogy support panel so v3 metadata stays compact above the map.

## Commands

- `python scripts/build_mindmap.py tests/fixtures/design-dense-korean.json -o .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
  - Result: `발표용`, `사회`, 8 branches.
- `python scripts/build_mindmap.py tests/fixtures/current-v2-valid.json -o .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `물의_순환_교과용.html`
  - Result: existing simple v2 fixture still builds.
- `python scripts/build_mindmap.py tests/fixtures/design-v3-pedagogy.json -o .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `알고리즘_사고_점검_마인드맵_퀴즈형.html`
  - Result: v3 pedagogy and quiz sample still builds.
- `python -m py_compile scripts/build_mindmap.py`
  - Exit: 0
- `python tests/test_build_mindmap.py`
  - Exit: 0
  - Result: 9 regression tests passed.
- `grep -En 'surface-wash|surface-guide|page-head|map-region-title|sr-only|vector-effect|repeating-linear-gradient' DESIGN.md assets/base-mindmap-template.html`
  - Exit: 0
  - Result: design tokens, page header, labelled map region, screen-reader heading, connector stability, and board guide lines are present.
- `grep -En 'radial-gradient|orb|bokeh|hero|product-card|marketplace|IDE|Miro|IBM|Apple|Cursor|Airbnb|Nike|Voltagent|Dell' assets/base-mindmap-template.html`
  - Exit: 1
  - Result: no prohibited brand/reference words or decorative radial/orb patterns in template CSS/markup.
- `grep -R -En '<main|<header class="page-head"|aria-labelledby="map-region-title"|class="lines"|class="node center"|vector-effect|data-mode|data-subject' .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Result: generated HTML includes landmarks, header, labelled map region, decorative connector SVG, center node, connector path attribute, and mode/subject data.
- `grep -R -En '{{[^}]+}}' .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out`
  - Exit: 1
  - Result: no unresolved placeholders.
- `grep -R -En 'orb|bokeh|hero|product-card|marketplace|IDE|Miro|IBM|Apple|Cursor|Airbnb|Nike|Voltagent|Dell' .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out assets/base-mindmap-template.html`
  - Exit: 1
  - Result: no prohibited words in generated output or template.
- `grep -R -En '<div class="node branch-' .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Result: dense sample renders 8 branches, v2 sample renders 4 branches, v3 pedagogy sample renders 4 branches.
- `grep -R -En 'radial-gradient|linear-gradient\(180deg, var\(--surface-wash\)|repeating-linear-gradient|background: var\(--surface-board\)' assets/base-mindmap-template.html .omo/evidence/task-4-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Result: output uses tokenized wash and board guide lines; no `radial-gradient` matches.
- `find . -type d -name __pycache__ -print`
  - Exit: 0 with no output after cleanup.

## Coverage Notes

- This todo verifies structure through generated HTML and source checks. Full visual/browser rendering, hover/focus state capture, reduced-motion emulation, and print screenshots remain intentionally deferred to Todo 8 and the final F3 gate.
- The generated output remains standalone single-file HTML/CSS/JS.
- No new framework, dependency, marketing hero, product tile, dark default, or brand clone was introduced.

## Adversarial QA

- `stale_state`: all three Todo 4 outputs were regenerated after the template edit.
- `dirty_worktree`: source changes are limited to `DESIGN.md` and `assets/base-mindmap-template.html`; generated HTML is retained under `.omo/evidence`.
- `misleading_success_output`: completion is based on build output, tests, source greps, generated HTML greps, and negative forbidden-pattern checks.
- `generated_artifacts`: generated Todo 4 HTML remains under `.omo/evidence/task-4.../out`.
- `hung_or_long_commands`: all commands completed within bounded tool timeouts.
- `scope_creep`: no adjacent worksheet, lesson-package, board-writing, presentation, game, timer, score, drag/drop, or physics behavior was added.

Cleanup: removed `scripts/__pycache__`; no server or browser session was started.
