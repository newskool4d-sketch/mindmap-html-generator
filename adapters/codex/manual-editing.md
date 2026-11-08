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
