# Gate Review - Task 8 Pass A Re-review

## recommendation

REJECT

## originalIntent

The user requested a read-only independent visual QA re-review Pass A for the mindmap-html-generator design upgrade after a CSS regression fix. The concrete regression was that generic `.node button:hover` / `.node button[aria-expanded="true"]` rules overrode nested `.quiz-toggle` controls, making quiz reveal buttons appear as blank white pills in prior screenshots.

## desiredOutcome

Confirm that branch-control styles are scoped to direct branch buttons (`.node > button`), quiz reveal buttons keep their own readable teal/white states, branch expansion still works, generated output remains real DOM/CSS rather than a pasted mock image, no unapproved design/mechanics drift was introduced, and responsive/print/focus/hover/active/reduced-motion/quiz-state evidence remains sufficient.

## userOutcomeReview

The specific visual regression appears fixed in the fresh source and screenshots. `assets/base-mindmap-template.html` uses `.node > button` for branch-control rules at lines 186, 198, 203, 207, 247, 617, and 667; `rg --fixed-strings ".node button"` found no remaining broad selector in the template or fresh generated output. `.quiz-toggle` keeps its own background/text/focus states at lines 340-366, and direct image inspection of the fresh `04-_-_-390x1200-quiz-open.png`, `04-_-_-390x1200-quiz-closed.png`, and `03-_-_-_-_-390x1200-quiz-open.png` shows readable teal buttons with white text.

Branch behavior remains supported by source and fresh browser evidence: JS still attaches branch expansion to branch nodes, browser metrics cover 4 samples, 28 checks, 112 captures, 3 viewports, print, reduced motion, and driven interaction states, with zero failures, zero horizontal overflow, zero overlaps, zero placeholder leakage, and zero overflow elements. Representative desktop/mobile/print screenshots show a real DOM/CSS mind-map surface, not a raster mock.

This review still rejects full gate approval because the required gate evidence package is incomplete and internally stale in places. The visual fix can be treated as passing this Pass A scope, but the final gate criteria are not satisfied by the artifact set.

## blockers

1. Code-review report coverage is missing the required skill-perspective check. `.omo/evidence/f2-code-quality-review.md` does not explicitly show `omo:remove-ai-slops` or `omo:programming` coverage, overfit/slop criteria, excessive/useless-test review, tautological/implementation-mirroring test review, or production slop review. The direct pass found no new visual/CSS slop blocker, but the report-coverage requirement is absent and unsupported.

2. The persistent evidence package is inconsistent with the fresh regression-fix run. `.omo/evidence/task-8-mindmap-html-generator-design-upgrade.md` still records screenshot run `2026-07-03T05-14-42-567Z`, while the fresh browser report inspected here was generated at `2026-07-03T08:15:42.972Z` and points to `2026-07-03T08-15-42-491Z`. `.omo/evidence/f3-real-manual-qa.md` still says `PARTIAL PASS` and references the older run.

3. The final-gate input/artifacts did not provide a notepad path. No notepad-path artifact was found in the inspected evidence sweep.

## directSlopAndProgrammingPass

Loaded and applied `omo:remove-ai-slops` and `omo:programming` criteria directly. I inspected the CSS selector fix, generated output selectors, `scripts/build_mindmap.py`, `tests/test_build_mindmap.py`, the diff/stat, and F2/F3 evidence. No deletion-only or request-removal-only tests were found as the reason for this visual fix; the tests exercise builder behavior, validation, v2/v3 compatibility, quiz rendering, escaping, and invalid fixtures. No unnecessary production extraction or new speculative abstraction was needed for the selector fix. The only slop/programming blocker is missing explicit coverage in the reviewed code-quality report.

## checkedArtifactPaths

- `assets/base-mindmap-template.html`
- `scripts/build_mindmap.py`
- `tests/test_build_mindmap.py`
- `DESIGN.md`
- `.omo/plans/mindmap-html-generator-design-upgrade.md`
- `.omo/evidence/f1-plan-compliance-audit.md`
- `.omo/evidence/f2-code-quality-review.md`
- `.omo/evidence/f3-blocker-audit.md`
- `.omo/evidence/f3-independent-visual-review-request.md`
- `.omo/evidence/f3-real-manual-qa.md`
- `.omo/evidence/f4-scope-fidelity.md`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade.md`
- `.omo/evidence/task-10-mindmap-html-generator-design-upgrade.md`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z/04-_-_-390x1200-quiz-open.png`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z/04-_-_-390x1200-quiz-closed.png`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z/03-_-_-_-_-390x1200-quiz-open.png`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z/01-_-_-_-_-_-_-_-1280x900-rest.png`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z/01-_-_-_-_-_-_-_-390x1200-rest.png`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z/01-_-_-_-_-_-_-_-1280x900-print.png`

## exactEvidenceGaps

- Missing explicit remove-ai-slops/programming/overfit coverage in `.omo/evidence/f2-code-quality-review.md`.
- Stale screenshot-run reference in `.omo/evidence/task-8-mindmap-html-generator-design-upgrade.md`.
- Stale partial-pass F3 status in `.omo/evidence/f3-real-manual-qa.md`.
- Missing notepad path in supplied or discovered artifacts.

