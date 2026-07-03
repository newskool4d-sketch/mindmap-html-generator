# Task 1 Evidence: hard v3 preflight and root DESIGN.md contract

## Current Rerun

Timestamp: 2026-07-03T12:20:00+09:00

Decision: v3 prerequisite present, DESIGN.md contract created.

The previous 2026-07-02 blocked result is retained below as historical evidence. It is superseded by this rerun after the v3 educational upgrade completed and F1-F4 final verification passed.

### Current Artifacts

- `DESIGN.md`
- `.omo/evidence/task-1-mindmap-html-generator-design-upgrade/v3-preflight.json`
- `.omo/evidence/task-1-mindmap-html-generator-design-upgrade/out/`

### Current Command Checklist

- `test -f references/educational-design.md`: exit 0.
- `test -f tests/test_build_mindmap.py`: exit 0.
- `grep -R -En "pedagogy|focus question|prior knowledge|misconception|vocabulary|transfer|assessment|초점|선수|오개념|어휘|전이|형성" references scripts assets tests`: exit 0, with matches in references, builder, template, fixtures, and tests.
- `python tests/test_build_mindmap.py`: exit 0, 9 tests passed.
- `python scripts/build_mindmap.py .omo/evidence/task-1-mindmap-html-generator-design-upgrade/v3-preflight.json -o .omo/evidence/task-1-mindmap-html-generator-design-upgrade/out`: exit 0.
- `grep -R -En "초점|오개념|어휘|전이|형성|focus|misconception|vocabulary|transfer|assessment" .omo/evidence/task-1-mindmap-html-generator-design-upgrade/out`: exit 0, generated HTML contains v3 pedagogy labels and values.
- `grep -R -En "pedagogy[^>]*>\\s*</|학습지원[^>]*>\\s*</" .omo/evidence/task-1-mindmap-html-generator-design-upgrade/out`: exit 1, no empty pedagogy shell.
- `test -f DESIGN.md`: exit 0.
- `grep -En "classroom whiteboard workspace|교실|화이트보드|Miro|IBM|Apple|Cursor|Airbnb|Do not clone|브랜드" DESIGN.md`: exit 0.
- `grep -En "^## (1[.] Atmosphere|2[.] Color|3[.] Typography|4[.] Spacing|5[.] Components|6[.] Motion|7[.] Depth)" DESIGN.md`: exit 0, all seven sections present.
- `grep -En "branch node|center node|connector|quiz|print|reduced-motion|focus|Branch Node|Center Node|Connector|Quiz|Print|Reduced" DESIGN.md`: exit 0, primitives/states covered.
- `grep -E "#ffd02f|#0f62fe|#0066cc|#ff385c|#f54e00|Voltagent|Nike Futura|Dell 1996" DESIGN.md`: exit 0 only for `Dell 1996` and `Voltagent` in `## Must Not Copy`; no exact brand color tokens or approved defaults found.
- `find . -type d -name __pycache__ -print`: checked after preflight cleanup; no cache artifact remains.

### Current Dirty Worktree Classification

- `.omo/`: planning, review, evidence, screenshots, and orchestration artifacts. Stage selectively if needed; do not use broad `git add .omo`.
- `references/educational-design.md`, `references/branch-archetypes.md`, `tests/`: intentional v3 prerequisite deliverables.
- `DESIGN.md`: intentional design-upgrade Todo 1 deliverable.
- `scripts/__pycache__/`: generated cache artifact; must be removed after test/preflight commands recreate it.

### Current Todo 1 State

Verified complete. Proceed to Todo 2.

---

## Historical Blocked Run

Timestamp: 2026-07-02T16:47:10+09:00

## Decision
v3 prerequisite missing

blocked - do not proceed to Todo 2

The reviewed design-upgrade plan requires v3 pedagogy metadata/schema/template/test artifacts before any design or template edits. The required v3 preflight files are absent, so `DESIGN.md` was not created and no template/source files were edited.

## Command Checklist

### `test -f references/educational-design.md`
- Exit: 1
- Result: missing

### `test -f tests/test_build_mindmap.py`
- Exit: 1
- Result: missing

### `grep -R -En "pedagogy|focus question|prior knowledge|misconception|vocabulary|transfer|assessment|초점|선수|오개념|어휘|전이|형성" references scripts assets tests`
- Exit: 2
- Stdout: `references/subject-themes.md:67:| 어휘/단어 | \`bi-translate\` |`
- Stderr: `grep: tests: No such file or directory`
- Result: failed as a v3 preflight because the `tests` path is absent and the required v3 schema/test/build proof is missing. The single `어휘/단어` subject-theme match is not sufficient v3 pedagogy evidence.

### `git status --short`
- Exit: 0
- Output:

```text
?? .omo/
?? scripts/__pycache__/
```

## Skipped Commands
- `python tests/test_build_mindmap.py`: skipped because `tests/test_build_mindmap.py` is missing.
- `python scripts/build_mindmap.py .omo/evidence/task-1-mindmap-html-generator-design-upgrade/v3-preflight.json -o .omo/evidence/task-1-mindmap-html-generator-design-upgrade/out`: skipped because the required v3 schema/test prerequisite is missing.
- Generated-output pedagogy grep: skipped because no v3 preflight output was generated.
- `DESIGN.md` acceptance greps: skipped because `DESIGN.md` must not be created until v3 preflight passes.

## Dirty Worktree Classification
- `.omo/`: planning, review, evidence, and orchestration artifacts for the current Codex/OMO workflow. These require selective staging decisions later; do not use broad `git add .omo`.
- `scripts/__pycache__/`: generated Python cache artifact. It should not be committed.

## Adversarial QA Notes
- `stale_state`: probed by reading the current filesystem and running the exact preflight file checks instead of relying on previous review memory.
- `dirty_worktree`: probed with `git status --short`; current untracked paths are classified above.
- `misleading_success_output`: the subject-theme grep match for `어휘/단어` was explicitly rejected as insufficient because required v3 files and test/build evidence are missing.
- `hung_or_long_commands`: four delegated workers failed to produce this evidence within wait windows; the fallback recorded only bounded local preflight checks and did not run long build/test commands after prerequisites failed.

## Final Todo 1 State
Blocked by missing v3 educational-upgrade artifacts. Stop before Todo 2 and before any design/template implementation.
