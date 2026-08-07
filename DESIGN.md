# Mindmap HTML Generator Design System

## 1. Atmosphere

The generated output should feel like a classroom whiteboard workspace: open, inspectable, calm, and clearly structured for Korean classroom learning. The signature is a warm whiteboard canvas with precise concept-map connectors, restrained public-sector clarity, and subject-color notes that support meaning without becoming decoration.

Reference weighting:
- Miro informs the spatial whiteboard/workspace logic and the idea of visible concept mapping.
- IBM informs public-sector clarity, strong contrast, thin borders, and disciplined information density.
- Apple informs restraint: the interface chrome should recede so the learning content is dominant.
- Cursor informs the warm neutral canvas, near-black text, light hairlines, and low-fatigue operational surface.
- Airbnb informs friendliness through spacing, approachable card rhythm, and modest softness.

Do not clone any brand identity. The reference files are inspiration, not source palettes, logos, proprietary typefaces, product chrome, or marketing layouts.

## 2. Color

### Palette

| Role | Token | Value | Usage |
| --- | --- | --- | --- |
| Canvas | `--surface-canvas` | warm near-white | Page background and classroom projection surface |
| Board | `--surface-board` | translucent white | Main whiteboard map region |
| Panel | `--surface-panel` | white | Pedagogy support panel and print-safe content blocks |
| Wash | `--surface-wash` | translucent white wash | Quiet page-level whiteboard light layer |
| Guide | `--surface-guide` | faint warm gray-green | Subtle board guide lines |
| Text primary | `--text-primary` | warm near-black | Titles, branch labels, body text |
| Text secondary | `--text-secondary` | muted green-gray | Descriptions, hints, secondary labels |
| Border subtle | `--border-subtle` | light warm gray-green | Panel boundaries and separators |
| Connector | `--line-connector` | muted subject-aware green-gray | Desktop connector lines |
| Focus | `--focus-ring` | high-contrast subject-aware ring | Keyboard focus and active state |
| Control | `--surface-control` / `--surface-control-hover` | translucent white | Toggle and quiz control states |
| Active border | `--border-active` | stronger warm gray-green | Expanded and active state boundary |
| Center start | `--center-start` | subject-aware middle tone | Center node gradient start |
| Center end | `--center-end` | subject-aware deep tone | Center node gradient end |
| Note 1-8 | `--surface-note-1` to `--surface-note-8` | soft subject-compatible tints | Branch note surfaces |
| Border on note | `--border-on-note` | translucent white | Branch note inner border |

### Subject Themes

Subject themes may shift `--center-*`, `--line-connector`, and `--note-*` tokens, but each theme must remain light by default, readable on projection, and printable. Theme color is a teaching cue, not brand decoration.

### Rules

- Use light surfaces by default. Do not make the generated map dark unless the user explicitly requests a special mode.
- Keep accent color tied to meaning: subject identity, focus, connector direction, or interaction state.
- Treat `--text-primary`, `--text-secondary`, `--focus-ring`, and `--surface-control` as contrast-sensitive tokens for classroom projection and keyboard use.
- Never use exact reference-brand colors as defaults.
- No bokeh, orbs, generic AI gradients, marketplace chrome, IDE mockups, campaign imagery, or retro stickers.

## 3. Typography

### Scale

| Level | Size | Weight | Line height | Tracking | Usage |
| --- | --- | --- | --- | --- | --- |
| Page title | 34-42px | 700 | 1.2 | 0 | Generated page heading |
| Center title | 34-46px | 700 | 1.2 | 0 | Center node title |
| Branch title | 20-23px | 700 | 1.35 | 0 | Branch labels |
| Body | 15-16px | 600-700 | 1.6-1.8 | 0 | Korean branch details |
| Support label | 13-14px | 700 | 1.45 | 0 | Pedagogy field labels |
| Hint | 14px | 600-700 | 1.6 | 0 | Bottom guidance |

### Font Stack

- Primary: `"Malgun Gothic", "맑은 고딕", system-ui, -apple-system, sans-serif`
- Icon font: Bootstrap Icons only when the generated HTML already loads it.
- Do not import proprietary reference fonts.

### Rules

- Letter spacing is 0 for normal Korean UI text.
- Use `word-break: keep-all` plus safe wrapping so Korean phrases stay readable but long tokens cannot overflow.
- Body text must not be hidden or shortened to pass visual QA.
- Display type stays moderate; this is a classroom artifact, not a marketing hero.

## 4. Spacing

### Base Unit

All spacing is based on 4px increments. Template work should migrate informal values into these token families before broad visual changes.

| Token | Value | Usage |
| --- | --- | --- |
| `--space-1` | 4px | Tight label spacing |
| `--space-2` | 8px | Icon and inline gaps |
| `--space-3` | 12px | Compact padding and list rhythm |
| `--space-4` | 16px | Button and branch inner spacing |
| `--space-5` | 20px | Page padding on small screens |
| `--space-6` | 24px | Panel rhythm |
| `--space-7` | 28px | Wide card inner spacing |
| `--space-8` | 32px | Map and section spacing |
| `--space-10` | 40px | Desktop breathing room |

### Layout

- Max page width remains wide enough for desktop mind maps, currently around 1500px.
- Desktop map composition may use absolute positioning for connector clarity.
- Tablet and mobile must stack nodes in document order with connector lines hidden.
- Print must expand all learning content and suppress only purely interactive controls.

## 5. Components

### Page Shell

- Structure: `main` wrapper, page title, description, optional pedagogy support panel, labelled map section, hint.
- States: default, print, mobile.
- Accessibility: Korean document language, semantic landmarks, no placeholder leakage.

### Pedagogy Support Panel

- Structure: optional `aside` with heading and labelled metadata items.
- States: absent, present, print, mobile.
- Accessibility: `aria-label="학습 지원 정보"` or equivalent.
- Rule: never render an empty shell when no metadata exists.

### Map Region

- Structure: labelled map `section`, hidden connector SVG, center node, branch nodes.
- States: desktop connector layout, tablet/mobile stack, print expansion.
- Accessibility: connector SVG is decorative and `aria-hidden`.

### Center Node

- Structure: circular or rounded focal node with title and support text.
- States: default, presentation mode, mobile, print.
- Rule: center node carries the concept anchor and must stay more prominent than branch notes.

### Branch Node

- Structure: colored note surface, button header, subtitle, collapsible detail list, optional quiz block.
- States: collapsed, expanded, hover, active/pressed, focus-visible, print.
- Accessibility: button has useful `aria-label`, stable `aria-controls`, and accurate `aria-expanded`.

### Branch Toggle

- Structure: compact icon-like control inside the branch header.
- States: plus, minus, hover, active/pressed, focus-visible.
- Rule: the toggle communicates state only; it must not introduce unrelated game or animation behavior.

### Quiz Reveal

- Structure: question, explicit answer button, hidden answer text.
- States: absent/not-applicable, closed, open, active/pressed, focus-visible, print.
- Rule: quiz content appears only when quiz data exists and quiz behavior has user approval.

### Hint Text

- Structure: short bottom instruction.
- States: default, quiz mode, print.
- Rule: guidance should describe the current artifact, not advertise features.

## 6. Motion

### Timing

| Type | Duration | Easing | Usage |
| --- | --- | --- | --- |
| Micro | 120-180ms | ease-out | Button press and hover affordance |
| Standard | 200-350ms | ease-in-out | Existing branch expansion |
| Control | 160ms | ease-out | Hover, active, and expanded control state |

### Rules

- Motion serves state changes only.
- Reduced motion disables non-essential transitions.
- Do not add autoplay, decorative motion, timers, scoring, game mechanics, drag/drop, physics, or staged reveal without explicit user approval.
- Avoid layout-shifting animation. Expansion behavior must remain predictable and tested.

### Motion & Radius Tokens (template-implemented)

| Token | Value | Usage |
| --- | --- | --- |
| `--motion-expand` | `max-height 0.35s ease, padding 0.35s ease` | Branch expand/collapse |
| `--motion-control` | 0.16s ease-out multi-property | Control hover/active/focus |
| `--radius-board` | 30px | Main board |
| `--radius-node` | 24px | Branch notes / center |
| `--radius-panel` | 18px | Pedagogy panel |
| `--radius-quiz` | 14px | Quiz block |
| `--radius-pill` | 999px | Toggle pill |

### Legacy Alias Layer

Subject themes override the legacy tokens `--bg`, `--panel`, `--text`, `--muted`, `--line`, `--center1/2`, `--card1`-`--card8`, `--shadow`. The semantic tokens above consume them via `var()` aliases (e.g. `--surface-canvas: var(--bg)`). This alias layer is the intentional theme-override surface; new CSS must reference the semantic tokens, never the legacy names directly.

## 7. Depth

### Strategy

Use mixed depth: tonal shift plus very soft shadows. Borders and hairlines carry most structure; shadows are low and broad to separate paper-like surfaces without producing card piles.

| Level | Token | Usage |
| --- | --- | --- |
| Flat | (`box-shadow: none` 직접 지정 — print/connector 전용 one-off) | Print and connector SVG |
| Panel | `--shadow-panel` | Pedagogy panel separation |
| Rest | `--shadow-rest` | Branch notes at rest |
| Board | `--shadow-board` | Main map board |
| Focus | `--shadow-focus` | Focused or expanded node when helpful |

### Rules

- Keep radius moderate and purposeful. Use larger radius only for the center node or touch-friendly notes.
- Do not nest UI cards inside other cards.
- Do not let shadows or translucency reduce Korean text contrast.
- Print removes decorative depth and keeps content structure.

## Must Not Copy

- Do not copy Miro wordmarks, canary-yellow branding, or exact board UI.
- Do not copy IBM Blue, IBM Plex as a required brand voice, or Carbon square austerity wholesale.
- Do not copy Apple product-gallery tiles, Action Blue, SF Pro branding, or marketing hero composition.
- Do not copy Cursor Orange, IDE chrome, code-editor mockups, or developer-tool campaign surfaces.
- Do not copy Airbnb Rausch, marketplace search bars, property cards, or booking UI.
- Do not use Dell 1996 retro frames, GIF-sticker vocabulary, Times body copy, or catalog density.
- Do not use Nike campaign typography, oversized uppercase commerce energy, or product retail chrome.
- Do not use Voltagent dark developer surfaces or electric-green AI-agent identity.
