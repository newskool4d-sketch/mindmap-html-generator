# Educational Design Reference

This reference defines the v3 pedagogy layer for mindmap HTML generation while preserving `v2 JSON 호환`.

## Fields

- grade band
- audience level
- focus question
- lesson purpose
- achievement-standard note
- prior knowledge
- misconceptions
- vocabulary support
- transfer/generalization prompt
- metacognitive prompt
- assessment prompt types

## Safe defaults

The pedagogy layer is optional and should enrich a normal v2 mindmap without changing the expected v2 JSON shape.

Automatic quizzes, timers, scores, games, staged reveal, and animation are not allowed by default.

## Assessment prompt types

Assessment prompt types may describe lightweight checks such as recall, explanation, comparison, evidence-based reasoning, misconception check, transfer, and reflection.

They should remain prompt-oriented and teacher-reviewable, not converted into automatic quiz systems or scored interactions by default.

## Deferred official curriculum mapping

Official Korean curriculum mapping is deferred for a future version and is not included now.

The `achievement-standard note` field may hold a plain human-authored note, but it must not claim verified official mapping.

## Guardrails

- Keep v2 fields usable without `pedagogy`.
- Treat all pedagogy fields as optional.
- Prefer teacher-facing prompts over automated activity mechanics.
- Do not infer official curriculum achievement standards automatically.
- Do not add automatic quizzes, timers, scores, games, staged reveal, or animation by default.

## JSON example

```json
{
  "title": "물의 순환",
  "description": "초등 과학 물의 순환 개념을 정리하는 마인드맵",
  "subject": "과학",
  "mode": "교과용",
  "center": {
    "title": "물의 순환",
    "text": "물이 상태와 위치를 바꾸며 지구 안에서 되풀이되는 과정"
  },
  "branches": [
    {
      "title": "증발",
      "sub": "물이 수증기로 바뀜",
      "icon": "bi-sun",
      "details": ["태양 에너지를 받아 물이 기체가 됨", "바다와 강, 젖은 땅에서 일어남"]
    },
    {
      "title": "응결",
      "sub": "수증기가 물방울로 바뀜",
      "icon": "bi-cloud",
      "details": ["높은 곳에서 차가워진 수증기가 작은 물방울이 됨", "구름 형성과 연결됨"]
    },
    {
      "title": "강수",
      "sub": "물이 다시 땅으로 내려옴",
      "icon": "bi-cloud-rain",
      "details": ["물방울이 무거워지면 비나 눈으로 내림", "내린 물은 다시 모이고 흐름"]
    }
  ],
  "hint": "원인과 결과를 연결해 보세요.",
  "pedagogy": {
    "grade_band": "elementary 3-4",
    "audience_level": "introductory",
    "focus_question": "물이 모습과 위치를 바꾸며 순환하는 이유는 무엇인가?",
    "lesson_purpose": "물의 순환 과정을 주요 개념과 관계 중심으로 설명한다.",
    "achievement_standard_note": "공식 교육과정 성취기준 매핑은 포함하지 않은 교사용 메모입니다.",
    "prior_knowledge": ["물의 세 가지 상태", "날씨 현상"],
    "misconceptions": ["구름은 수증기 자체라는 오해", "증발은 끓을 때만 일어난다는 오해"],
    "vocabulary_support": ["증발", "응결", "강수", "수증기"],
    "transfer_generalization_prompt": "컵의 물이 줄어드는 현상을 물의 순환과 연결해 설명해 보세요.",
    "metacognitive_prompt": "내가 헷갈린 단계는 무엇이고, 어떤 연결을 다시 확인해야 할까요?",
    "assessment_prompt_types": ["explanation", "misconception check", "transfer", "reflection"]
  }
}
```
