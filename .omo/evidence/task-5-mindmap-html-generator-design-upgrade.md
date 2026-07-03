# Task 5 Evidence: component states for nodes, controls, and pedagogy panels

Timestamp: 2026-07-03T13:50:00+09:00

Verdict: complete

## Artifacts

- `DESIGN.md`
- `assets/base-mindmap-template.html`
- `scripts/build_mindmap.py`
- `.omo/evidence/task-5-mindmap-html-generator-design-upgrade/out/기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
- `.omo/evidence/task-5-mindmap-html-generator-design-upgrade/out/알고리즘_사고_점검_마인드맵_퀴즈형.html`

## What changed

- Documented control-state tokens in `DESIGN.md`: `--surface-control`, `--surface-control-hover`, and `--border-active`.
- Expanded component-state language for branch nodes, branch toggles, and quiz reveal to include active/pressed and absent/not-applicable where relevant.
- Added tokenized hover, active/pressed, expanded, and focus-visible visual states for branch nodes, branch buttons, branch icons, quiz toggles, and opened quiz answers.
- Added stable `data-label` values to branch and quiz buttons so JavaScript can update `aria-label` when a branch is expanded/collapsed or a quiz answer is opened/closed.
- Added `aria-controls` and an `id` for quiz answer text.
- Marked branch toggle icons `aria-hidden="true"` because button labels already communicate the state.
- Removed the previous `backdrop-filter` use so the plan's forbidden `drop` grep does not falsely match a non-drag/drop CSS property.

## Commands

- `python -m py_compile scripts/build_mindmap.py`
  - Exit: 0
- `python tests/test_build_mindmap.py`
  - Exit: 0
  - Result: 9 regression tests passed.
- `python scripts/build_mindmap.py tests/fixtures/design-dense-korean.json -o .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
  - Result: dense 8-branch sample still builds.
- `python scripts/build_mindmap.py tests/fixtures/design-v3-pedagogy.json -o .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Output file: `알고리즘_사고_점검_마인드맵_퀴즈형.html`
  - Result: v3 pedagogy plus quiz sample still builds.
- `grep -R -En 'aria-expanded|focus-visible|quiz-toggle|정답 보기|정답 닫기|data-label|aria-hidden="true"|--motion-control|--surface-control|--border-active|초점|오개념|어휘|전이' DESIGN.md assets/base-mindmap-template.html scripts/build_mindmap.py .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Result: documented states, CSS state selectors, generated ARIA/data attributes, quiz open/closed labels, hidden icons, and v3 pedagogy labels are present.
- `grep -R -En 'drag|drop|timer|score|autoplay|physics|setInterval' assets/base-mindmap-template.html .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out`
  - Exit: 1
  - Result: no unapproved mechanics.
- `grep -R -En 'requestAnimationFrame' assets/base-mindmap-template.html .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Classification: existing layout refresh path only; no new animation mechanic, timer, score, game, physics, or staged reveal.
- `grep -R -En '접기|자세히 보기|정답 닫기|aria-controls="branch-1-quiz-answer"|quiz-a hidden|<aside class="pedagogy"' assets/base-mindmap-template.html scripts/build_mindmap.py .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out`
  - Exit: 0
  - Result: dynamic branch labels, quiz answer labels, quiz answer id/control relation, hidden answer state, and v3 pedagogy panel are present.
- `grep -R -En '<aside class="pedagogy"' .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out/기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
  - Exit: 1
  - Result: no empty pedagogy shell in the dense sample without pedagogy metadata.
- `grep -R -En '{{[^}]+}}' .omo/evidence/task-5-mindmap-html-generator-design-upgrade/out`
  - Exit: 1
  - Result: no unresolved placeholders.
- `grep -En -- '--motion-control:.*(width|height|top|left|right|bottom|margin)' assets/base-mindmap-template.html`
  - Exit: 1
  - Result: new control state transitions do not animate layout properties. Existing branch expansion still uses the pre-existing `--motion-expand` path.
- `git diff --check`
  - Exit: 0
  - Result: no whitespace errors; Git reported line-ending warnings only.
- `find . -type d -name __pycache__ -print`
  - Exit: 0 with no output after cleanup.

## Coverage Notes

- This task did not add new interaction mechanics. It refined the states of existing branch expansion and approved quiz answer reveal.
- Visual/browser state screenshots remain intentionally deferred to Todo 8 and final F3.
- Print state remains covered by existing print CSS; Todo 7 will refine print layout further.

## Adversarial QA

- `stale_state`: dense and v3 outputs were regenerated after CSS/JS/builder changes.
- `dirty_worktree`: source changes are limited to design contract, template, and builder; generated HTML remains under `.omo/evidence`.
- `misleading_success_output`: completion is based on tests, generated markup, source greps, negative mechanic grep, placeholder grep, and cache cleanup.
- `generated_artifacts`: generated HTML is retained only under `.omo/evidence/task-5.../out`.
- `hung_or_long_commands`: all verification commands completed within bounded tool timeouts.
- `scope_creep`: no new timer, score, game, drag/drop, physics, autoplay, or staged reveal behavior was introduced.

Cleanup: removed `scripts/__pycache__`; no server or browser session was started.
