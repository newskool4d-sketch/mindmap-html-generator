# F4 Scope Fidelity

## Verdict

APPROVE.

## Checked Scope

The skill remains an HTML/node concept-map generator:

- JSON spec to standalone HTML output
- Center node, branch nodes, connector lines
- 교과용 / 발표용 / 퀴즈형 rendering modes
- Optional v3 pedagogy support panel
- Subject themes and icons
- Approved quiz answer reveal only when quiz data exists

## Out-of-Scope Guardrails Preserved

Docs and routing references still hand off or reject adjacent work:

- Board-writing / chalkboard zoning: `board-writing-generator`
- Print worksheet: `html-worksheet-generator`
- Lesson package: `class-total-package`
- PBL lesson design: `pbl-lesson-designer`
- Rubric / assessment table: relevant assessment/document skill

## Verification

- `adapters/codex/references/routing-smoke-test.md` still requires an HTML, node/branch, visual mind-map, or interactive concept-map output boundary.
- Focused negative grep for over-triggering on generic `개념도` passed.
- No docs make retro/campaign/developer/marketplace/orb/brand-clone styling the default; those appear only as guardrails or failure signals.
