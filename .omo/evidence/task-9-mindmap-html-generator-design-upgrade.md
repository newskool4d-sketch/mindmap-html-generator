# Task 9 Evidence - Docs Aligned To Design Contract

## Verdict

PASS.

README, root skill, Codex adapter, and relevant references now point future workers to `DESIGN.md` before visual/template changes and preserve the classroom whiteboard workspace direction.

## Files Updated

- `README.md`
- `SKILL.md`
- `adapters/codex/SKILL.md`
- `adapters/codex/references/layout-interaction-rules.md`
- `adapters/codex/references/routing-smoke-test.md`
- `references/output-modes.md`

## What Changed

- Added `DESIGN.md` to the shared repository/core asset contract and Codex sync list.
- Documented `classroom whiteboard workspace` as the default design direction.
- Added brand-reference limits: reference folders are inspiration, not permission to copy palettes, logos, product chrome, marketplace cards, IDE mockups, marketing heroes, or retro/campaign/developer aesthetics.
- Added browser visual QA expectations after template/design changes: 1280px+, 768px, 375-390px, print, reduced motion, branch states, and quiz states when present.
- Preserved routing boundaries: this skill remains for HTML/node/branch mind-map outputs, with adjacent lesson/worksheet/board/rubric work handed to adjacent skills.

## Verification

```bash
grep -R -En "DESIGN\.md|classroom whiteboard workspace|화이트보드|visual QA|브랜드|brand|clone|whiteboard" README.md SKILL.md adapters/codex/SKILL.md adapters/codex/references/layout-interaction-rules.md adapters/codex/references/routing-smoke-test.md references/output-modes.md
```

Result: exit 0. Matches appeared in the intended docs and references.

```bash
if grep -R -En "개념도.*(always|trigger|항상|무조건)|((always|항상|무조건).*개념도)" README.md SKILL.md adapters/codex/SKILL.md adapters/codex/references/layout-interaction-rules.md adapters/codex/references/routing-smoke-test.md references/output-modes.md; then
  echo "routing over-trigger instruction found"
  exit 1
else
  echo "routing over-trigger negative check passed"
fi
```

Result: exit 0, `routing over-trigger negative check passed`.

## Notes

- A broader drift grep intentionally found terms like `retro`, `campaign`, `developer`, `marketplace`, `bokeh`, `orb`, `generic AI gradient`, and `brand-clone` only in guardrail/failure-signal contexts.
- No Codex-only `apply_patch` or handoff instructions were copied into the root skill beyond the existing file-handling note already present in this repo.
