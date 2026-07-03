# F3 Real Manual QA

## Verdict

PASS.

Browser rendering, fresh visual QA metrics, direct screenshot inspection, and independent read-only visual reviews all pass after the final quiz-toggle regression fix.

## Browser Evidence

- Report: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json`
- Screenshot run: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z`
- Samples: 4
- Screenshots: 112
- Viewports: 1280x900, 768x1000, 390x1200
- States: rest, hover, focus-visible, active/pressed, expanded mid-transition, expanded settled, collapsed, quiz open, quiz closed, reduced motion, print
- Automated browser verdict: PASS

## Direct Screenshot Inspection

Inspected representative screenshots from the fresh `2026-07-03T08-15-42-491Z` run:

- Dense Korean desktop rest: 8 branch nodes, connector lines, no overlap, no horizontal overflow.
- Dense Korean mobile rest: stacked layout, readable Korean wrapping, no horizontal scroll.
- v3 pedagogy + quiz desktop open: support panel renders only with metadata, quiz answer opens inside the branch.
- v3 pedagogy + quiz mobile open: panel and branches stack without clipping.
- Quiz sample mobile open/closed: `정답 닫기` and `정답 보기` render as readable teal controls with white text after the `.node > button` selector fix.
- Print emulation: branch details and quiz answers expand; connector/control-only UI is suppressed.

## Regression Fix

Fresh independent review found that generic `.node button` rules were overriding `.quiz-toggle` hover/open styles, producing blank-looking white pill controls in quiz states.

Fix applied in `assets/base-mindmap-template.html`: branch-control selectors were scoped from `.node button` to `.node > button`, including responsive and print rules, so nested quiz reveal controls keep their dedicated styling.

Verification after the fix:

- Selector grep shows generic branch styling only targets `.node > button`.
- `PYTHONUTF8=1 python -m py_compile scripts/build_mindmap.py`: PASS.
- `PYTHONUTF8=1 python tests/test_build_mindmap.py`: PASS, 9 tests.
- Fresh browser visual QA: PASS, 4 samples, 28 checks, 112 screenshots, 0 failures.

## Independent Review

The user explicitly approved read-only independent visual review subagents.

- Pass A, design-system/functionality re-review (`019f2716-5a2b-7f73-8a46-1ac0357b0efc`): PASS, HIGH confidence, no findings, no blocking items.
- Pass B, visual/CJK/mobile/print re-review (`019f270e-80e1-7071-8cbd-6c9eb6968106`): PASS, HIGH confidence, no findings, no blocking items.

## Gate Result

F3 is satisfied. The implementation has fresh browser evidence after the last edit, direct screenshot inspection, and independent reviewer PASS results.
