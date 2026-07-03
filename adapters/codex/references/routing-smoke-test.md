# Routing Smoke Test

Use this file to regression-check whether `mindmap-html-generator` stays focused on HTML mind maps rather than all concept organization requests.

## Must Trigger

- `수업용 HTML 마인드맵 만들어줘`
- `개념도를 인터랙티브 mind map 형태로 만들어줘`
- `발표용 가지형 개념 정리를 웹으로 보여주고 싶어`
- `branching topic summary를 HTML/CSS/JS로 만들어줘`
- `과학 물의 순환을 정리용 HTML 노드 개념도로 만들어줘`
- `복습용 마인드맵에 초점 질문과 오개념 점검도 넣어줘`
- `평가 전 자기 점검용 퀴즈형 마인드맵 만들어줘` (quiz approval still required before adding quiz data)

## Must Not Trigger

- `칠판 판서안을 만들어줘`
- `PBL 수업안 설계해줘`
- `탐구 보고서 수행평가 기준표를 만들어줘`
- `판서안과 평가까지 포함한 수업팩을 만들어줘`
- `개념도 없이 수업 흐름만 단계별로 짜줘`
- `수업 정리 학습지를 인쇄용으로 만들어줘`
- `평가 루브릭과 채점 기준표를 만들어줘`
- `마인드맵도 포함한 전체 차시 운영계획을 만들어줘`

## Adjacent Skills

- `board-writing-generator`
- `html-worksheet-generator`
- `class-total-package`
- `pbl-lesson-designer`

## Boundary Checks

- Output is an HTML mind map or concept map with visual node structure.
- `개념도`, `수업 정리`, `복습`, `평가`, `탐구` alone are not enough; the request must still ask for an HTML, node/branch, visual mind-map, or interactive concept-map output.
- Visual styling requests for this skill should preserve root `DESIGN.md` and the classroom whiteboard workspace unless the user explicitly asks for a different design direction.
- Design reference folders are inspiration only; do not treat a brand/style name as permission to clone logos, exact palettes, product chrome, marketplace cards, IDE mockups, or marketing hero layouts.
- ultra-short direct request: `마인드맵만`
- If the request is for classroom board text or chalkboard zoning, hand off to `board-writing-generator`.
- If the request is for a lesson flow or project design, hand off to `pbl-lesson-designer`.
- If the request is for a print-ready worksheet, hand off to `html-worksheet-generator`.
- If the request is for a rubric or assessment standard table rather than a node map, hand off to the relevant assessment/document skill.
- ultra-short mixed-module non-match: `판서+마인드맵`
- If the request bundles the mind map with other lesson outputs, hand off to `class-total-package`.

## Failure Signals

- The skill starts matching any request that contains `개념도` even when HTML output is not intended.
- The skill absorbs general classroom layout requests that belong to board-writing.
- The body loses the visual-output boundary and becomes a generic concept-summary skill.
- The default visual direction drifts into retro, campaign, developer-console, marketplace, bokeh/orb, generic AI gradient, or brand-clone styling.
