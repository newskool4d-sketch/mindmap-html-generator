---
name: mindmap-html-generator
description: Use when the user asks in Korean for a 마인드맵, 개념도, 가지형 정리, 수업용 개념 시각화, 발표용 마인드맵, or HTML/CSS/JS mind map. Create Korean HTML mind maps optimized first for laptop and desktop viewing while still remaining readable on mobile, with Malgun Gothic typography, safe node spacing, and an explicit confirmation step before adding animation or quiz features.
metadata:
  short-description: 데스크톱 우선 한국어 HTML 마인드맵 생성기
---

# Mindmap HTML Generator

Use this skill when the user asks for any of the following in Korean or mixed Korean/English:

- `마인드맵 만들어줘`
- `개념도 그려줘`
- `가지형으로 정리해줘`
- `중심 주제에서 뻗는 형태로 만들어줘`
- `수업용 개념 시각화`
- `발표용 마인드맵`
- `html 마인드맵`
- `인터랙티브 마인드맵`

Also trigger it for English or mixed requests such as:

- `mind map`
- `concept map`
- `interactive HTML mind map`
- `branching topic summary`

Read these bundled files only when needed:

- For a reusable starter file, use [assets/base-mindmap-template.html](assets/base-mindmap-template.html)
- For choosing an output style, use [references/output-modes.md](references/output-modes.md)

## What this skill produces

- A standalone HTML file by default
- A central-topic mind map with branch nodes connected by visible lines
- A layout optimized first for laptop and desktop screens
- A secondary responsive layout that remains readable on mobile
- Korean text styled with `Malgun Gothic` first
- Click-to-expand branch content when interaction is helpful

## Required defaults

Apply these unless the user explicitly asks otherwise.

- Use `font-family: "Malgun Gothic", "맑은 고딕", sans-serif;`
- Use bold weight for major labels and titles
- Differentiate sizes by importance:
  - page title: largest
  - central topic: second largest
  - branch titles: medium
  - detail bullets: smallest
- Use calm, low-saturation colors that are easy on the eyes
- Keep strong contrast between text and background
- Prevent overlap between nodes, labels, connector lines, and expanded content
- Design for desktop first, then add mobile-safe fallback behavior
- Ensure bottom branches and expanded panels are not clipped by the container
- Keep connector lines visually attached to the related nodes without awkward gaps
- Prefer computed connector lines based on actual node positions instead of hard-coded SVG coordinates
- Do not let Korean words or short phrase units break awkwardly in the middle of a line
- Prefer line wrapping that moves the next whole word or phrase unit to the next line instead of splitting it

## Mandatory confirmation rule

Before adding either of the following, ask the user in plain Korean first:

- animation
- quiz elements

Use a short direct question such as:

- `애니메이션도 넣을까요?`
- `퀴즈 요소도 함께 넣을까요?`

If the user has not explicitly approved them, do not add them.

## Subject parameter (교과 테마)

When a subject is known, set `data-subject` on `<html>` and apply the matching theme.

Supported values and detection:

| `data-subject` | 감지 키워드 |
|----------------|------------|
| `국어` | 국어, 문학, 독서, 글쓰기, 언어 |
| `수학` | 수학, 대수, 기하, 확률, 통계, 함수 |
| `과학` | 과학, 물리, 화학, 생물, 지구, 생명, 환경 |
| `사회` | 사회, 지리, 경제, 정치, 법, 문화 |
| `영어` | 영어, English, 영문, 회화 |
| `미술` | 미술, 미학, 조형, 색채, 드로잉, 디자인 |
| `음악` | 음악, 악기, 리듬, 화음, 멜로디 |
| `체육` | 체육, 스포츠, 건강, 운동 |
| `역사` | 역사, 한국사, 세계사, 근현대사 |
| `도덕` | 도덕, 윤리, 인성, 가치관 |

Rules:
- When subject is explicitly provided by the user or parent skill, use it directly.
- When subject is not provided but the topic contains one of the detection keywords, infer the subject.
- When subject cannot be determined, omit `data-subject` and use the default green theme.
- Do not ask the user to confirm the inferred subject — apply silently and mention it in one line at the end.

Bootstrap Icons usage:
- The template already loads Bootstrap Icons CDN.
- In branch `node-title`, replace the text label with an icon + label pattern when a relevant icon exists.
- Use `<i class="bi bi-{icon-name}"></i>` inline before the label text.
- Icon recommendations per subject: see [references/subject-themes.md](references/subject-themes.md)
- Keep icons small and consistent — do not resize or recolor icons individually.
- If no suitable icon exists for a branch, omit the icon rather than using a generic one.

Branch icon pattern (with Bootstrap Icons):

```html
<div class="node-title">
  <span><i class="bi bi-book"></i> 개념 정의</span>
  <span class="icon">+</span>
</div>
```

## Output workflow

1. Identify the learning topic, subject, and target audience level.
2. Determine subject theme from explicit input or keyword inference.
3. Draft the branch structure before coding.
4. Choose the interaction level:
   - static mind map
   - clickable expand/collapse
   - animated or quiz-enhanced only after approval
   - when the user wants a mode, select from `교과용`, `발표용`, `퀴즈형`
4. Build responsive HTML with embedded CSS and small JS only when needed.
5. Verify that the desktop layout has no collisions.
6. Verify that the mobile layout remains readable and tap-friendly.
7. Verify that expanded lower nodes are fully visible and not cut off at the bottom.
8. Recompute connector lines from the current node positions whenever the layout changes.

## Branch structure guidance

Prefer 3 to 5 main branches by default.
Allow up to 8 branches when the topic genuinely needs finer separation.

For school-oriented concept maps, good default buckets are:

- meaning or definition
- importance or purpose
- core categories
- rules or limits
- examples or applications
- summary or key takeaway

Keep branch labels short. Keep detailed bullets to one line when possible.

When the user does not choose a mode, default to `교과용`.

Branch count guidance:

- 3 to 5 branches: default and recommended for most outputs
- 6 branches: acceptable when the topic has several equally important categories
- 7 to 8 branches: allowed, but keep each branch concise and only use them when compression would hide important distinctions
- if the source material is too dense, combine adjacent ideas before exceeding 8 branches

## Layout rules

Desktop and laptop are the primary target:

- Place the main topic in the center
- Distribute branches to left and right or radially
- Draw connector lines behind the nodes
- Align connector endpoints so the lines appear attached to the node edges
- Use JS to measure the center node and branch nodes, then draw connector lines from those measured positions
- Give each node enough width and padding to avoid cramped text
- Keep expanded content from colliding with nearby nodes
- Prefer a fixed scenic layout over a narrow mobile-first stack
- Reserve enough bottom space for expanded lower branches
- Increase container height or reposition lower nodes when expanded content risks being clipped
- Use text wrapping rules that avoid mid-word breaks and keep Korean text visually natural

Mobile is a fallback view:

- Switch to a stacked or simplified layout only at narrower widths
- Remove or hide connector lines if they reduce clarity
- Keep tap targets large enough for touch use
- Preserve reading order from top to bottom

If the user explicitly asks for a sample output, create a full HTML file from the base template and adapt it to the topic instead of replying with abstract guidance only.

## Styling rules

- Prefer soft greens, beige, muted blue, warm gray, or other low-fatigue tones
- Avoid neon, overly saturated colors, and heavy dark themes unless asked
- Use rounded cards and soft shadows sparingly
- Keep the center node visually distinct from branch nodes
- Apply CSS such as `word-break: keep-all;` and `overflow-wrap: normal;` to text containers unless the user explicitly needs a different rule

## Interaction rules

Default interactive behavior:

- branch click toggles detail content

Keep JS minimal and readable.

Preferred connector strategy:

- add a `data-connect` attribute to each branch node
- measure the center node and each branch node with `getBoundingClientRect()`
- convert the measured positions into map-local coordinates
- draw or redraw SVG paths after load and on resize
- recalculate after expand/collapse transitions and element resize events
- skip decorative connector lines on narrow mobile layouts if they reduce clarity

When filling `{{BRANCHES}}` in the base template, every branch node should include either:

- `data-connect="left"`
- `data-connect="right"`

Recommended branch markup pattern:

```html
<div class="node branch-1" data-connect="left">
  <button type="button">
    <div class="node-title">
      <span>1. Branch Title</span>
      <span class="icon">+</span>
    </div>
    <div class="node-sub">Short subtitle</div>
  </button>
  <div class="content">
    <ul>
      <li>Detail point</li>
      <li>Detail point</li>
    </ul>
  </div>
</div>
```

Use `branch-1` through `branch-8` for branch color styling.

Do not add:

- drag-and-drop
- physics-based motion
- autoplaying animation
- timed quiz flows

unless the user explicitly asks and confirms.

## File handling

When the user wants the result saved locally, create a standalone `.html` file in the requested folder.

Use the `Write` tool to create new files and the `Edit` tool for modifications.

## Quality checklist

Before finishing, confirm all of the following:

- subject theme applied (or default used) and noted in one line
- topic is reflected correctly
- central and branch hierarchy is clear
- text uses `Malgun Gothic` first
- title and importance levels have different font sizes
- desktop nodes do not overlap
- connector lines visually meet the related nodes and do not float apart from them
- connector lines are computed from current node positions, not frozen to outdated manual coordinates
- lower expanded nodes are not clipped by the canvas or outer container
- line wrapping does not split Korean words or short phrase units awkwardly in the middle
- mobile view is still readable
- animation and quiz features were only added after explicit approval
