# Layout And Interaction Rules

## Branch Structure

- Prefer 3 to 5 main branches by default.
- Allow up to 8 branches only when compression would hide important distinctions.
- Good school-oriented buckets: meaning, importance, categories, rules, examples, applications, key takeaway.
- Keep branch labels short and detailed bullets to one line when possible.

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
- Use `word-break: keep-all;` and `overflow-wrap: normal;` for Korean text unless another rule is needed.

## Interaction

- Default interaction: branch click toggles detail content.
- Keep JS minimal and readable.
- Use `data-connect="left"` or `data-connect="right"` on branch nodes.
- Redraw connectors after load, resize, expand/collapse, and element resize events.
- Use `branch-1` through `branch-8` for branch color styling.
- Do not add drag-and-drop, physics motion, autoplay animation, or timed quiz flows unless explicitly requested and confirmed.
