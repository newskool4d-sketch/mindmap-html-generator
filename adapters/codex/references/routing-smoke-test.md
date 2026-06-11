# Routing Smoke Test

Use this file to regression-check whether `mindmap-html-generator` stays focused on HTML mind maps rather than all concept organization requests.

## Must Trigger

- `수업용 HTML 마인드맵 만들어줘`
- `개념도를 인터랙티브 mind map 형태로 만들어줘`
- `발표용 가지형 개념 정리를 웹으로 보여주고 싶어`
- `branching topic summary를 HTML/CSS/JS로 만들어줘`

## Must Not Trigger

- `칠판 판서안을 만들어줘`
- `PBL 수업안 설계해줘`
- `탐구 보고서 수행평가 기준표를 만들어줘`
- `판서안과 평가까지 포함한 수업팩을 만들어줘`

## Adjacent Skills

- `board-writing-generator`
- `class-total-package`
- `pbl-lesson-designer`

## Boundary Checks

- Output is an HTML mind map or concept map with visual node structure.
- ultra-short direct request: `마인드맵만`
- If the request is for classroom board text or chalkboard zoning, hand off to `board-writing-generator`.
- If the request is for a lesson flow or project design, hand off to `pbl-lesson-designer`.
- ultra-short mixed-module non-match: `판서+마인드맵`
- If the request bundles the mind map with other lesson outputs, hand off to `class-total-package`.

## Failure Signals

- The skill starts matching any request that contains `개념도` even when HTML output is not intended.
- The skill absorbs general classroom layout requests that belong to board-writing.
- The body loses the visual-output boundary and becomes a generic concept-summary skill.
