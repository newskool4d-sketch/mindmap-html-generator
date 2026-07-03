# Task 8 Evidence - Fresh Browser Visual QA

## Verdict

PASS.

Visual QA skill-guided browser pass completed after the latest template edit. The run used a real Playwright browser, captured fresh screenshots, drove interaction states, and wrote objective metrics.

After the user approved read-only independent visual review subagents, two independent reviews also passed on the fresh evidence.

## Samples

- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/out/물의_순환_교과용.html`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/out/기후_변화의_원인과_대응_전략_한눈에_정리_발표용.html`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/out/알고리즘_점검_퀴즈형.html`
- `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/out/알고리즘_사고_점검_마인드맵_퀴즈형.html`

Coverage: v2 simple, dense Korean, 8 branches, 발표용, 퀴즈형, v3 pedagogy metadata, and quiz reveal.

## Commands

```bash
OUT=.omo/evidence/task-8-mindmap-html-generator-design-upgrade/out
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/current-v2-valid.json -o "$OUT"
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/design-dense-korean.json -o "$OUT"
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/quiz-approved.json -o "$OUT"
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/design-v3-pedagogy.json -o "$OUT"
node .omo/evidence/task-8-mindmap-html-generator-design-upgrade/visual-qa.mjs --sample-dir "$OUT" --viewports 1280,768,390 --states rest,hover,focus-visible,active,expanded,collapsed,quiz-open,quiz-closed,reduced-motion,print --out .omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots
```

Result: exit 0.

## Browser Evidence

- Report: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json`
- Screenshot run: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z`
- Samples checked: 4
- Browser checks: 28
- Screenshots captured: 112
- Viewports: 1280x900, 768x1000, 390x1200
- States captured: rest, hover, focus-visible, active/pressed, expanded mid-transition, expanded settled, collapsed, quiz open, quiz closed, reduced motion, print
- Automated verdict: PASS
- Failures: none

## Visual Inspection Notes

- Desktop dense Korean sample: no node overlap, no horizontal overflow, connector lines remain visually attached and clear.
- Mobile dense Korean sample: no horizontal scroll; center node and eight branch nodes stack in document order; Korean title wraps without clipping.
- v3 pedagogy + quiz sample: support panel is present only when metadata exists; quiz answer opens inside the branch without covering adjacent content.
- Print emulation: branch content and quiz answers expand; connector SVG, toggle icons, hint, and quiz buttons are suppressed as intended.
- Reduced motion: checked across all samples and viewports; no failures were reported in transition/motion metrics.

## Fixes Made During QA

- The first browser run exposed two QA precision issues:
  - `sr-only` text was incorrectly counted as visible text overflow.
  - Print expansion was visually correct but `overflow: visible` was not explicit in print CSS.
- Fixes:
  - Excluded `.sr-only` from visual overflow metrics in the Todo 8 harness.
  - Added `overflow: visible !important` to print `.content` rules in `assets/base-mindmap-template.html`.
- A later independent review exposed one real CSS regression:
  - Generic `.node button` branch-control rules overrode nested `.quiz-toggle` hover/open styles, causing quiz reveal buttons to appear as blank white pills.
- Fix:
  - Scoped branch-control selectors to `.node > button` in `assets/base-mindmap-template.html`, including responsive and print rules.
  - Regenerated all four representative samples and reran browser visual QA.
  - Directly inspected fresh mobile quiz open/closed screenshots; `정답 보기` and `정답 닫기` are readable.

## Independent Review

- Pass A, design-system/functionality re-review: PASS, HIGH confidence, no findings, no blocking items.
- Pass B, visual/CJK/mobile/print re-review: PASS, HIGH confidence, no findings, no blocking items.

## Acceptance Mapping

- Fresh screenshots after latest template edit: yes.
- Desktop/tablet/mobile widths: yes.
- Branch rest/hover/focus-visible/active/expanded/collapsed states: yes.
- Quiz open/closed states: yes, on quiz-bearing samples.
- Reduced-motion emulation: yes.
- Print emulation: yes.
- No unresolved placeholders: browser report placeholder count 0.
- No horizontal mobile scroll: browser report horizontal overflow false for all checks.
- PASS source: visual QA skill-guided real browser run plus direct screenshot inspection.
