---
name: mindmap-html-generator
description: Use when the user asks in Korean for a 마인드맵, 개념도, 가지형 정리, 수업용 개념 시각화, 발표용 마인드맵, or HTML/CSS/JS mind map. Create Korean HTML mind maps from a JSON spec via the bundled builder script, with 13 subject themes, 교과용/발표용/퀴즈형 modes, optional v3 pedagogy metadata, desktop-first layout, Malgun Gothic typography, a classroom whiteboard workspace design contract, and an explicit confirmation step before adding animation or quiz features.
metadata:
  short-description: 데스크톱 우선 시각형 HTML 마인드맵 생성기 (v3 — JSON 빌더·교육 설계·교과 테마·모드)
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
- `mind map` / `concept map` / `interactive HTML mind map` / `branching topic summary`

If the user wants classroom board zoning or chalkboard flow, hand off to `board-writing-generator`.
If the user wants a PDF textbook turned into a print-ready HTML worksheet rather than a node-based concept map, hand off to `html-worksheet-generator`.
If the user wants the mind map bundled with other lesson outputs, hand off to `class-total-package`.

Read these bundled files only when needed:

- [scripts/build_mindmap.py](scripts/build_mindmap.py) — JSON spec → HTML auto-builder (preferred path)
- [assets/base-mindmap-template.html](assets/base-mindmap-template.html) — template for manual editing
- [DESIGN.md](DESIGN.md) — generated HTML design contract (classroom whiteboard workspace)
- [references/educational-design.md](references/educational-design.md) — v3 pedagogy metadata contract and safe defaults
- [references/branch-archetypes.md](references/branch-archetypes.md) — subject and lesson-purpose branch defaults
- [references/output-modes.md](references/output-modes.md) — mode specs (교과용·발표용·퀴즈형)
- [references/subject-themes.md](references/subject-themes.md) — per-subject icon recommendations
- [references/layout-interaction-rules.md](references/layout-interaction-rules.md) — detailed layout/interaction rules
- [references/routing-smoke-test.md](references/routing-smoke-test.md) — trigger boundary regression checks
- For shared design behavior, use the `common-operating-rules` reference `references/design-artifact-principles.md`

## Workflow

1. Identify the topic, subject, grade band, and audience level — reflect the level in bullet vocabulary and depth.
2. Decide the lesson purpose — `도입`, `정리`, `복습`, `평가`, or `탐구`; this is separate from rendering `mode`.
3. Draft the optional pedagogy layer: focus question, prior knowledge, misconception risk, vocabulary support, transfer/generalization prompt, metacognitive prompt, and assessment prompt types as needed.
4. Choose a branch structure from [references/branch-archetypes.md](references/branch-archetypes.md), combining the subject archetype with the lesson-purpose archetype.
5. Decide the subject theme (detection table below) — use it as given when stated, infer from keywords otherwise, fall back to the default theme when undecidable.
6. Decide the output mode — default `교과용`. Selection criteria: [references/output-modes.md](references/output-modes.md).
7. Ask before quiz or animation. Do not add a `quiz` key or extra motion until explicitly approved.
8. Write a JSON spec and run `python scripts/build_mindmap.py spec.json -o <output folder>` (preferred).
   Only copy and edit the template manually when the builder cannot be used.
9. Verify with the quality checklist below.

File naming: `주제_모드.html` (e.g. `광합성_교과용.html`) — the builder applies this automatically.

## Design Contract

Before changing template CSS, layout, interaction states, print behavior, or reduced-motion behavior, read
[DESIGN.md](DESIGN.md). The default direction is a **classroom whiteboard workspace**: a warm whiteboard canvas,
precise concept-map connectors, low-fatigue classroom projection colors, Korean readability, and a restrained
public-education hierarchy.

Miro, IBM, Apple, Cursor, and Airbnb-style references are inspiration and weighting only. Do not copy palettes,
logos, product chrome, marketing hero layouts, marketplace cards, IDE mockups, retro/campaign/developer aesthetics,
bokeh/orbs, or generic AI gradients. If a needed token or state is missing, update `DESIGN.md` first and then use it.

## Auto-build (preferred)

Save the JSON spec as UTF-8 and run the builder. The full spec format is in the docstring at the top of `build_mindmap.py`.

```json
{
  "title": "광합성", "description": "한 줄 설명", "subject": "과학", "mode": "교과용",
  "center": {"title": "광합성", "text": "중심 보조 설명"},
  "branches": [
    {"title": "개념", "sub": "부제", "icon": "bi-atom", "details": ["불릿 1", "불릿 2"]},
    {"title": "과정", "details": ["..."]}
  ],
  "pedagogy": {
    "grade_band": "초등 5-6",
    "audience_level": "introductory",
    "focus_question": "광합성은 왜 식물과 생태계에 중요할까?",
    "lesson_purpose": "정리",
    "achievement_standard_note": "human-authored teacher note; not automatic official mapping",
    "prior_knowledge": ["식물의 구조", "빛과 에너지"],
    "misconceptions": ["식물은 흙을 먹고 자란다는 오개념"],
    "vocabulary_support": ["엽록체", "이산화탄소", "포도당"],
    "transfer_generalization_prompt": "햇빛이 부족한 환경과 연결해 설명해 보세요.",
    "metacognitive_prompt": "내가 헷갈린 연결은 무엇인가요?",
    "assessment_prompt_types": ["explanation", "misconception check", "transfer"]
  }
}
```

`pedagogy` is optional. When absent, v2 JSON output remains unchanged. When present, only non-empty
fields render in a compact learning-support panel. Do not automatically claim official curriculum mapping.

Add `"quiz": {"q": "질문", "a": "정답"}` to a branch **only after explicit user approval**
(do not put a quiz key in the spec while unapproved).

The builder handles automatically: left/right distribution (alternating when unspecified, left gets +1 when odd), HTML escaping, branch count validation (max 8), warning + default theme for unsupported subjects, `data-subject` attribute removal, and file naming.

## Mandatory confirmation rule (animation · quiz)

Before adding either of the following, ask the user in plain Korean first:

- animation (staged reveal, autoplay, motion effects)
- quiz elements

Use a short direct question such as `애니메이션도 넣을까요?` / `퀴즈 요소도 함께 넣을까요?`
If the user has not explicitly approved them, do not add them. If you cannot ask, treat as unapproved.

**No approval needed for**: the template's built-in click expand/collapse and its 0.35s transition —
this is default behavior, not animation.

## Subject themes (data-subject)

`data-subject` must be set on the `<html>` tag (setting it elsewhere breaks the theme — see subject-themes.md).

| `data-subject` | Detection keywords |
|----------------|--------------------|
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
| `정보` | 정보, 인공지능, AI, 데이터, 코딩, SW, 소프트웨어, 컴퓨터, 디지털 |
| `실과` | 실과, 기술가정, 기술·가정, 가정, 요리, 의생활, 식생활 |
| `진로` | 진로, 직업, 자기이해, 진학, 커리어 |

Rules:

- Apply an inferred subject silently without asking — mention it in one line at the end
  (do the same one-line mention when the default theme was used).
- When the subject cannot be determined, delete the `data-subject` attribute entirely and use the
  default green theme (do not leave an empty `data-subject=""`).

Icons: the template loads the Bootstrap Icons CDN. Add `<i class="bi bi-{name}"></i>` **before** the
branch title label (not replacing the label text). Per-subject recommendations: subject-themes.md.
Skip the icon when no semantically fitting one exists — do not force it. Offline, a CDN failure
only blanks the icons; the layout holds.

## Branch structure

- Prefer 3–5 branches; max 8. Use 6 when there are several peer categories, 7–8 only when
  compression would erase an important distinction. Never exceed 8 — merge adjacent concepts instead.
- Left/right distribution: alternate, left gets one more when odd (builder handles this).
- Standard school concept-map buckets: meaning/definition → importance/purpose → key categories →
  rules/limits → examples/applications → key takeaway.
- Use [references/branch-archetypes.md](references/branch-archetypes.md) for subject and lesson-purpose defaults, but do not expand this skill into a full lesson plan, board plan, worksheet, or assessment rubric.
- Keep branch labels short, bullets one line when possible, no numbering (`1.`) in branch titles.

## Manual editing reference (builder not used)

Template placeholders:

| Placeholder | Content |
|-------------|---------|
| `{{TITLE}}` | Page title (shared by h1 and `<title>`) |
| `{{DESCRIPTION}}` | One-line description under the title |
| `{{SUBJECT}}` | Subject name — delete the whole attribute when undecided |
| `{{MODE}}` | `교과용` / `발표용` / `퀴즈형` |
| `{{CENTER_TITLE}}` / `{{CENTER_TEXT}}` | Center circle title / supporting text |
| `{{PEDAGOGY}}` | Optional pedagogy metadata panel — empty string when absent |
| `{{BRANCHES}}` | Branch node markup (pattern below) |
| `{{HINT}}` | Bottom hint (default: "각 가지 카드를 클릭하면 자세한 내용이 열립니다.") |

Branch markup pattern — `data-connect="left|right"` is the **left/right column placement** attribute
(connector lines are drawn automatically for every non-center `.node`, independent of data-connect):

```html
<div class="node branch-1" data-connect="left">
  <button type="button" aria-controls="branch-1-content" aria-label="브랜치 제목 자세히 보기">
    <div class="node-title">
      <span><i class="bi bi-book"></i> 브랜치 제목</span>
      <span class="icon">+</span>
    </div>
    <div class="node-sub">짧은 부제</div>
  </button>
  <div id="branch-1-content" class="content">
    <ul><li>불릿</li></ul>
  </div>
</div>
```

Classes `branch-1`–`branch-8` set the card colors. In a single-file deliverable you may remove the
unused `[data-subject]` theme blocks (leave builder output untouched).

## Style and layout invariants

- Follow the `DESIGN.md` classroom whiteboard workspace tokens and states
- `font-family: "Malgun Gothic", "맑은 고딕", sans-serif` / bold for major labels
- Font size hierarchy: page title > center topic > branch title > bullets
- Calm, low-saturation colors (neon/oversaturated/dark themes only on request), strong text contrast
- `word-break: keep-all; overflow-wrap: anywhere; overflow-x: hidden;` — preserves Korean readability while preventing mobile overflow
- Compute connector lines from actual node positions (no hard-coding) — the template JS recomputes on resize/expand
- No drag-and-drop, physics motion, autoplay animation, or timed quizzes without explicit request + approval
- No brand-clone colors, logos, product chrome, bokeh/orbs, generic AI gradients, or marketing hero composition as defaults
- For detailed branch, layout, styling, and interaction rules, read [references/layout-interaction-rules.md](references/layout-interaction-rules.md).

## File handling

When the user wants the result saved locally, create a standalone `.html` file in the requested folder.

Use `apply_patch` for file creation or edits. Run the builder with `python scripts/build_mindmap.py`.

## Quality checklist

Confirm all of the following before finishing:

- [ ] Subject theme applied (or default theme) + one-line mention at the end
- [ ] Mode reflected in `data-mode`
- [ ] Lesson purpose is chosen separately from rendering mode
- [ ] Focus question, prior knowledge, misconception risk, and vocabulary support are included in `pedagogy` when useful
- [ ] Branch structure fits the subject and lesson purpose and stays within 8 branches
- [ ] Topic and hierarchy (center > branches) are correct
- [ ] Missing `pedagogy` creates no empty support panel or labels
- [ ] No desktop node overlap / no clipped bottom nodes / connector lines touch the nodes
- [ ] No mid-word Korean line breaks / mobile stays readable
- [ ] Animation and quiz added only after approval
- [ ] Visual/template changes match `DESIGN.md`
- [ ] Visual/template changes have browser visual QA at 1280px+, 768px, 375-390px, print, reduced motion, branch states, and quiz states when present

Verification: open the file in a browser when possible and check desktop (1280px+), tablet (768px), and mobile
(375-390px), plus print/reduced-motion, branch expand/collapse, and quiz answer open/closed states. If browser
verification is unavailable, verify by code review and state
"렌더링 미검증" when reporting.

Code-review caveat: the `data-connect` string also appears twice in the template's built-in JS
querySelectors, so count branches with the `<div class="node branch-` pattern. The template's
`requestAnimationFrame` is built-in connector-recompute code, not "autoplay animation".
