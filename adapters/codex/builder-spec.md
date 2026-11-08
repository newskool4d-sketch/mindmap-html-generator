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
