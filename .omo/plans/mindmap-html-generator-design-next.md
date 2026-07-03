# Mindmap HTML Generator Design Next Plan

## Objective

Improve the generated HTML mind map from a verified v3 design system into a more resilient classroom artifact: clearer at a glance, easier to inspect on projectors and mobile screens, and safer to extend without visual regressions.

## Current Baseline

- Root `DESIGN.md` defines the classroom whiteboard workspace contract.
- `assets/base-mindmap-template.html` now uses token-backed surfaces, connector layout, branch states, quiz states, print expansion, and reduced-motion handling.
- Fresh Playwright visual QA passed with 4 samples, 28 checks, and 112 screenshots.
- Independent visual reviews passed after the `.node > button` selector fix.

## Non-Goals

- Do not turn the skill into a lesson-plan, worksheet, board-writing, PBL, assessment-rubric, or presentation-theme generator.
- Do not add automatic quizzes, timers, scoring, drag/drop, physics, staged reveal, autoplay, or decorative motion without explicit user approval.
- Do not copy Miro, IBM, Apple, Cursor, Airbnb, or any other brand's palette, logo, product chrome, or marketing composition.
- Do not commit generated screenshot PNGs or generated HTML output by default.

## Phase D1: Visual System Tightening

Acceptance:

- `DESIGN.md` names every reusable color, radius, spacing, focus, depth, and motion token used in the template.
- Template CSS has no reusable raw values that bypass the design contract, except one-off layout geometry that is documented as such.
- Subject themes preserve Korean text contrast on projectors and in print.

QA:

- Grep for raw color literals and new untokened spacing/radius patterns after each template change.
- Regenerate dense Korean and quiz samples, then run browser visual QA at 1280px, 768px, and 390px.

## Phase D2: Classroom Readability Upgrade

Acceptance:

- Dense Korean samples remain readable without mid-word Korean breaks, clipped text, or horizontal mobile scroll.
- Branch title, subtitle, details, quiz question, and answer each have distinct hierarchy without relying on color alone.
- Projector mode at 1280px and classroom print output are treated as first-class views.

QA:

- Add at least one intentionally long Korean title fixture and one vocabulary-heavy fixture.
- Capture desktop, tablet, mobile, and print screenshots after the last edit.

## Phase D3: Component State Showcase

Acceptance:

- A small generated showcase or QA fixture covers branch collapsed, expanded, hover, focus-visible, active, quiz closed, quiz open, absent pedagogy, present pedagogy, and print states.
- The showcase remains generated from the same builder/template path, not a hand-authored mock.

QA:

- Browser QA must drive all states and fail on blank controls, invisible focus, clipped quiz answers, unresolved placeholders, or horizontal overflow.

## Phase D4: Pedagogy Panel Refinement

Acceptance:

- The pedagogy panel helps teachers/students scan focus question, prior knowledge, misconceptions, vocabulary, transfer, metacognition, and assessment prompts without becoming a separate lesson plan.
- Empty or partial pedagogy data creates no empty labels, empty shells, or awkward gaps.
- Mobile and print layouts keep the panel useful without pushing the concept map out of view.

QA:

- Add fixtures for no pedagogy, one-field pedagogy, and full pedagogy.
- Verify each fixture with browser QA and unit tests.

## Phase D5: Evidence and Release Hygiene

Acceptance:

- `.gitignore` keeps generated HTML, screenshot PNGs, caches, and older research output out of commits by default.
- Evidence Markdown plus the latest visual QA report remain commit-friendly.
- README release checks match the actual validation commands.

QA:

- `git status --short --ignored` shows intended source/evidence files as trackable and generated artifacts as ignored.
- `git diff --check`, Python compile, unit tests, placeholder grep, mechanic grep, and visual QA all pass before commit.

## Review Gate

Before any future design implementation is called complete:

- Run the generated samples through real browser visual QA after the last edit.
- Inspect at least one desktop, one mobile, one quiz, and one print screenshot manually.
- Ask for or run an independent read-only visual review when the change affects template layout, controls, or responsive behavior.
