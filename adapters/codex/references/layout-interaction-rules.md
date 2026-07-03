# Layout And Interaction Rules

## Design Contract

- Follow root `DESIGN.md` before changing layout, CSS tokens, component states, print behavior, or reduced-motion behavior.
- The default visual direction is a classroom whiteboard workspace: warm light canvas, precise concept-map connectors, low-fatigue subject color, and Korean classroom readability.
- Miro, IBM, Apple, Cursor, and Airbnb references are inspiration only. Do not copy brand palettes, logos, product chrome, marketplace cards, IDE mockups, marketing hero layout, retro/campaign/developer aesthetics, bokeh/orbs, or generic AI gradients.

## Branch Structure

- Prefer 3 to 5 main branches by default.
- Allow up to 8 branches only when compression would hide important distinctions.
- Choose subject and lesson-purpose defaults from `references/branch-archetypes.md` before drafting labels.
- Good school-oriented buckets: meaning, importance, categories, rules, examples, applications, key takeaway.
- Lesson purpose is separate from rendering mode: `도입`, `정리`, `복습`, `평가`, and `탐구` shape branch content, while `교과용`, `발표용`, and `퀴즈형` shape rendering.
- Keep branch labels short and detailed bullets to one line when possible.
- Do not expand a branch archetype into a full lesson plan, board-writing plan, worksheet, PBL plan, or assessment rubric.

## Layout

- Desktop and laptop are the primary targets.
- Place the main topic in the center and distribute branches left/right or radially.
- Draw connector lines behind nodes and align endpoints to node edges.
- Use JS measurement with `getBoundingClientRect()` instead of hard-coded SVG coordinates.
- Keep expanded content from colliding with nearby nodes or being clipped.
- On mobile, switch to stacked or simplified layout and hide connector lines when they reduce clarity.

## Styling

- Prefer low-fatigue tones and avoid neon, heavy dark themes, and oversaturated palettes unless asked.
- Keep the center node visually distinct.
- Use `word-break: keep-all; overflow-wrap: anywhere; overflow-x: hidden;` for Korean readability and mobile overflow protection.
- Keep style changes token-backed by `DESIGN.md`; add the token there before introducing a new reusable color, spacing, radius, depth, focus, or motion value.

## Pedagogy Panel

- Render `pedagogy` only when at least one supported field has content.
- Keep the panel compact and teacher/student supportive: focus question, prior knowledge, misconception check, vocabulary support, transfer prompt, metacognitive prompt, and assessment prompt types.
- Do not claim official curriculum achievement-standard mapping unless the user supplies verified text.
- Missing pedagogy must not leave empty labels, empty cards, or unresolved template placeholders.

## Interaction

- Default interaction: branch click toggles detail content.
- Keep JS minimal and readable.
- Use `data-connect="left"` or `data-connect="right"` on branch nodes.
- Redraw connectors after load, resize, expand/collapse, and element resize events.
- Use `branch-1` through `branch-8` for branch color styling.
- Do not add drag-and-drop, physics motion, autoplay animation, or timed quiz flows unless explicitly requested and confirmed.
- Branch buttons need programmatically useful labels and controlled content ids; quiz answer buttons need explicit answer-toggle labels.

## Visual QA

- After template or design changes, generate representative HTML outputs and run real browser visual QA.
- Required coverage: 1280px or wider, 768px, 375-390px, print emulation, reduced-motion emulation, branch rest/hover/focus/active/expanded/collapsed, and quiz open/closed when quiz data exists.
- Do not claim final visual quality from grep, tests, or code review alone. If browser tooling is unavailable, record `렌더링 미검증`.
