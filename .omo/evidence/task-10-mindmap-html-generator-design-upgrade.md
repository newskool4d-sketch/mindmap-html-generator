# Task 10 Evidence - Cleanup, Regression, Plan Audit

## Verdict

PASS.

The full available regression suite passes, browser QA remains clean, generated cache artifacts were removed, and `.omo` artifacts are classified for staging hygiene.

## Commands

```bash
E=.omo/evidence/task-10-mindmap-html-generator-design-upgrade
OUT="$E/out"
PYTHONUTF8=1 python -m py_compile scripts/build_mindmap.py
PYTHONUTF8=1 python tests/test_build_mindmap.py
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/current-v2-valid.json -o "$OUT"
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/design-dense-korean.json -o "$OUT"
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/design-v3-pedagogy.json -o "$OUT"
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/quiz-approved.json -o "$OUT"
```

Result: exit 0. `tests/test_build_mindmap.py` ran 9 tests and reported `OK`.

```bash
PYTHONUTF8=1 python scripts/build_mindmap.py tests/fixtures/design-invalid-too-many-branches.json -o "$OUT/invalid"
```

Result: expected non-zero. Log contains `[오류] 브랜치 9개 — 최대 8개`.

```bash
! grep -R -En "\{\{[^}]+\}\}" "$OUT"
! grep -R -En "#ffd02f|#0f62fe|#0066cc|#ff385c|#f54e00|Voltagent|Nike Futura|Dell 1996" assets "$OUT"
! grep -R -En "drag|drop|timer|score|autoplay|physics|setInterval" assets/base-mindmap-template.html "$OUT"
! grep -En "font-size:[^;]*vw|h-screen|transition:[^;]*(width|height|top|left|right|bottom|margin)" assets/base-mindmap-template.html
node -e "const r=require('./.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json'); if(r.summary.verdict!=='PASS') process.exit(1); console.log('Todo8 browser visual QA PASS with', r.samples.length, 'samples');"
git diff --check
```

Result: exit 0. `git diff --check` emitted only line-ending warnings about LF becoming CRLF when Git touches files.

## Cleanup

- Removed `scripts/__pycache__` after verifying the resolved absolute path stayed inside the workspace.
- Verified no `__pycache__` directories remain under `scripts` or `tests`.
- `git status --short` no longer lists `scripts/__pycache__/`.

## Generated Evidence

- Todo 8 browser screenshots: 112 PNGs under `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/2026-07-03T08-15-42-491Z`.
- Todo 8 report: `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/screenshots/browser-visual-qa-report.json`.
- Todo 8 generated samples: 4 HTML files under `.omo/evidence/task-8-mindmap-html-generator-design-upgrade/out`.
- Todo 10 generated samples: 4 HTML files under `.omo/evidence/task-10-mindmap-html-generator-design-upgrade/out`.
- Invalid-fixture log: `.omo/evidence/task-10-mindmap-html-generator-design-upgrade/invalid-too-many-branches.log`.

## `.omo` Classification

Commit-friendly current design-plan artifacts:

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

Ignored/local evidence artifacts:

- `.omo/evidence/**/out/*`
- `.omo/evidence/**/screenshots/20*/*`
- `.omo/evidence/f3-real-manual-qa/*`
- `.omo/drafts/*`
- `.omo/frontend-design/*`
- `.omo/evidence/task-*-mindmap-html-generator-upgrade.md`
- `.omo/plans/mindmap-html-generator-upgrade.md`
- `.omo/ulw-research/*`
- `.omo/start-work/ledger.jsonl`
- `.omo/boulder.json`

Staging guidance: do not use broad `git add .omo`. Stage the commit-friendly Markdown, the QA harness, and the latest JSON report; keep generated HTML/screenshots uncommitted unless the user explicitly wants evidence artifacts committed. `.gitignore` now encodes this split.

## Plan Conformance

- Todos 1-10 have evidence files.
- Todo 8 is backed by fresh browser screenshots and `browser-visual-qa-report.json` PASS after the latest template edit.
- Todo 9 docs align README, root skill, Codex adapter, and routing/layout references with `DESIGN.md`.
- No unresolved placeholders, unapproved brand tokens, or unapproved mechanics were found in generated outputs.
- Final verification wave F1-F4 is complete.
