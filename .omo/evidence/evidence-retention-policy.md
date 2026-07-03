# Evidence Retention Policy

## Verdict

Keep concise, reviewable evidence in git. Keep generated HTML, screenshots, cache files, and older research output local unless the user explicitly asks to publish those artifacts.

## Commit

- `.omo/plans/mindmap-html-generator-design-upgrade.md`
- `.omo/plans/mindmap-html-generator-design-next.md`
- `.omo/evidence/evidence-retention-policy.md`
- `.omo/evidence/task-1-mindmap-html-generator-design-upgrade.md` through `.omo/evidence/task-10-mindmap-html-generator-design-upgrade.md`
- `.omo/evidence/f1-plan-compliance-audit.md`
- `.omo/evidence/f2-code-quality-review.md`
- `.omo/evidence/f3-real-manual-qa.md`
- `.omo/evidence/f4-scope-fidelity.md`
- `.omo/evidence/high-accuracy-review-summary-mindmap-html-generator-design-upgrade.md`
- `.omo/evidence/plan-self-review-mindmap-html-generator-design-upgrade.md`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json`

## Keep Local

- `.omo/evidence/**/out/**`
- `.omo/evidence/**/screenshots/20*/**`
- `.omo/evidence/f3-real-manual-qa/**`
- `.omo/drafts/**`
- `.omo/ulw-research/**`
- `.omo/start-work/**`
- `.omo/boulder.json`
- `scripts/__pycache__/`, `tests/__pycache__/`, and `*.pyc`

## Rationale

The committed evidence should prove what changed and how it was verified without turning the repository into an artifact archive. The latest browser report records the visual QA result, sample count, state coverage, and failure list; the screenshot PNGs remain available locally for inspection but are excluded from git because they are generated, bulky, and reproducible from the harness.

## Current Latest Visual QA

- Report: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json`
- Screenshot run kept local: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z`
- Samples: 4
- Checks: 28
- Screenshots: 112
- Verdict: PASS
