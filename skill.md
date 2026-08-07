---
name: mindmap-html-generator
description: |
  한국어 HTML 마인드맵 생성 스킬. JSON 스펙 → 자동 빌드 스크립트, 13개 교과 테마,
  교과용·발표용·퀴즈형 모드, v3 교육 설계 메타데이터, 데스크톱 우선 레이아웃,
  맑은고딕 타이포그래피, classroom whiteboard workspace 디자인 계약 지원.
  사용자가 "마인드맵 만들어줘", "개념도 그려줘", "가지형으로 정리해줘",
  "수업용 개념 시각화", "발표용 마인드맵", "퀴즈 마인드맵", "HTML 마인드맵",
  "인터랙티브 마인드맵", "mind map", "concept map", "체험학습 개념도",
  "수업 정리 마인드맵" 등을 언급하면 이 스킬을 사용할 것.
  주제를 시각적으로 구조화하거나 브랜치 형태로 정리해달라는 요청이면
  스킬 이름을 언급하지 않더라도 이 스킬을 사용할 것.
---

# Mindmap HTML Generator

> **정본(Claude)**: 이 개발 repo(`.git` 포함)가 편집 정본. `~/.codex/skills/mindmap-html-generator/`는 경량 미러. 수정은 Claude에서 하고 필요 시 Codex로 동기화한다.

중심 주제 + 좌우 브랜치 노드 + 연결선으로 구성된 단일 HTML 파일을 생성한다.
데스크톱 우선, 모바일은 세로 나열 폴백. 인쇄 시 전체 펼침 레이아웃 내장.

번들 파일 (필요할 때만 읽을 것):

- [scripts/build_mindmap.py](scripts/build_mindmap.py) — JSON 스펙 → HTML 자동 생성 (권장 경로)
- [assets/base-mindmap-template.html](assets/base-mindmap-template.html) — 수동 편집용 템플릿
- [DESIGN.md](DESIGN.md) — 생성 HTML의 시각 디자인 계약 (classroom whiteboard workspace)
- [references/educational-design.md](references/educational-design.md) — v3 교육 설계 메타데이터와 안전 기본값
- [references/branch-archetypes.md](references/branch-archetypes.md) — 교과·수업 목적별 브랜치 기본 구조
- [references/output-modes.md](references/output-modes.md) — 모드별 스펙 (교과용·발표용·퀴즈형)
- [references/subject-themes.md](references/subject-themes.md) — 교과별 아이콘 추천 목록

## Workflow

1. 주제·교과·학년군/대상 수준 파악 — 대상 수준은 불릿의 어휘 난이도와 내용 깊이에 반영
2. 수업 목적을 정함 — `도입`, `정리`, `복습`, `평가`, `탐구` 중 하나로 생각하되, 이는 렌더링 `mode`와 별개
3. 초점 질문, 선수 지식, 오개념 위험, 어휘 지원, 전이·메타인지·형성 확인 프롬프트를 필요한 만큼 정함
4. [references/branch-archetypes.md](references/branch-archetypes.md)에서 교과와 수업 목적에 맞는 브랜치 구조를 고르고, 주제에 맞게 줄임
5. 교과 테마 결정 (아래 감지 표) — 명시되면 그대로, 키워드 매칭되면 추론, 불가하면 기본 테마
6. 출력 모드 결정 — 기본 `교과용`. 선택 기준은 [references/output-modes.md](references/output-modes.md)
7. 퀴즈·애니메이션이 필요한 경우 먼저 승인 확인. 승인 전에는 `quiz` 키나 별도 모션을 넣지 않음
8. JSON 스펙 작성 → `python scripts/build_mindmap.py spec.json -o 출력폴더` 실행 (권장).
   빌더를 쓸 수 없는 경우에만 템플릿을 직접 복사·편집
9. 품질 체크리스트 검증 (아래)

파일명 규칙: `주제_모드.html` (예: `광합성_교과용.html`) — 빌더가 자동 적용.

## 디자인 계약

템플릿 CSS, 레이아웃, 상호작용 상태, print/reduced-motion 규칙을 바꿀 때는 먼저
[DESIGN.md](DESIGN.md)를 읽는다. 기본 시각 방향은 **classroom whiteboard workspace**:
따뜻한 화이트보드 캔버스, 명확한 개념 연결선, 낮은 피로도의 교실 투사용 색, 한국어 가독성,
공공 교육 자료에 맞는 절제된 정보 위계다.

Miro, IBM, Apple, Cursor, Airbnb 계열 레퍼런스는 영감과 가중치일 뿐이다. 팔레트, 로고,
제품 UI, 마케팅 hero, marketplace 카드, IDE chrome, retro/campaign/developer 미학을
기본값으로 복제하지 않는다. 필요한 색·간격·상태가 없으면 템플릿에 임의 값을 넣기 전에
`DESIGN.md`에 토큰이나 규칙을 먼저 추가한다.

v3.1부터 절제된 스큐어모피즘(종이 질감 스티키 노트·테이프·화이트보드 프레임·데스크톱 미세 기울기)과
전 교과 테마 6색 이상 노트 팔레트가 기본이다. 스큐어모피즘 큐는 CSS 전용이며 인쇄 시 평면화된다.

## 자동 생성 (권장)

JSON 스펙을 UTF-8로 저장 후 빌더 실행. 스펙 형식 전체는 `build_mindmap.py` 상단 docstring 참조.

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
    "achievement_standard_note": "공식 성취기준 자동 매핑이 아닌 교사용 참고 메모",
    "prior_knowledge": ["식물의 구조", "빛과 에너지"],
    "misconceptions": ["식물은 흙을 먹고 자란다는 오개념"],
    "vocabulary_support": ["엽록체", "이산화탄소", "포도당"],
    "transfer_generalization_prompt": "햇빛이 부족한 환경과 연결해 설명해 보세요.",
    "metacognitive_prompt": "내가 헷갈린 연결은 무엇인가요?",
    "assessment_prompt_types": ["explanation", "misconception check", "transfer"]
  }
}
```

`pedagogy`는 모두 선택 필드. 없으면 기존 v2 JSON 출력처럼 작동하고, 값이 있는 항목만
작은 학습 지원 패널로 렌더링한다. 공식 교육과정 성취기준은 자동 매핑하지 않는다.

퀴즈는 **사용자 승인 후에만** 브랜치에 `"quiz": {"q": "질문", "a": "정답"}` 키를 추가
(미승인 상태에서 spec에 quiz 키를 넣지 말 것).

빌더가 자동 처리하는 것: 좌/우 배분(미지정 시 교대, 홀수면 왼쪽 +1), HTML 이스케이프,
브랜치 수 검증(최대 8), 교과 미지원 시 경고 후 기본 테마, `data-subject` 속성 제거, 파일명 생성.

## 필수 확인 규칙 (애니메이션·퀴즈)

다음을 추가하기 전에 반드시 한국어로 먼저 물을 것:

- 애니메이션 (staged reveal, 자동 재생, 모션 효과)
- 퀴즈 요소

질문 예: `애니메이션도 넣을까요?` / `퀴즈 요소도 함께 넣을까요?`
명시적 승인이 없으면 추가하지 않는다. 사용자에게 물을 수 없는 상황이면 미승인으로 간주.

**승인이 필요 없는 것**: 템플릿에 내장된 클릭 expand/collapse와 그 0.35s 트랜지션은
기본 동작이며 애니메이션으로 간주하지 않는다.

## 교과 테마 (data-subject)

`data-subject`는 반드시 `<html>` 태그에 설정 (다른 요소에 달면 테마 깨짐 — 이유는 subject-themes.md).

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
| `정보` | 정보, 인공지능, AI, 데이터, 코딩, SW, 소프트웨어, 컴퓨터, 디지털 |
| `실과` | 실과, 기술가정, 기술·가정, 가정, 요리, 의생활, 식생활 |
| `진로` | 진로, 직업, 자기이해, 진학, 커리어 |

규칙:

- 추론한 교과는 사용자에게 확인하지 말고 조용히 적용 — 마지막에 한 줄로만 언급
  (기본 테마를 쓴 경우에도 동일하게 한 줄 언급)
- 교과 판단 불가 시 `data-subject` 속성 자체를 삭제하고 기본 그린 테마 사용
  (빈 문자열 `data-subject=""`로 남기지 말 것)

아이콘: 템플릿이 Bootstrap Icons CDN을 로드함. 브랜치 제목 라벨 **앞에** `<i class="bi bi-{name}"></i>`를
추가 (라벨 텍스트를 대체하는 것이 아님). 교과별 추천은 subject-themes.md.
의미가 맞는 아이콘이 없으면 생략 — 억지로 끼워 넣지 않는다. 오프라인 환경에서는
CDN 실패 시 아이콘만 빈칸 처리되고 레이아웃은 유지됨.

## 브랜치 구조

- 기본 3~5개 권장, 최대 8개. 6개는 동급 카테고리가 여럿일 때, 7~8개는 압축하면 중요한
  구분이 사라질 때만. 8개를 넘기지 말고 인접 개념을 통합할 것
- 좌/우 배분: 교대 배치, 홀수면 왼쪽에 1개 더 (빌더 자동 처리)
- 학교 개념도의 기본 버킷: 의미/정의 → 중요성/목적 → 핵심 분류 → 규칙/한계 → 예시/적용 → 핵심 정리
- 교과·수업 목적별 기본 구조는 [references/branch-archetypes.md](references/branch-archetypes.md)를 참고하되,
  전체 수업안·판서안·학습지·평가기준표로 확장하지 말 것
- 브랜치 라벨은 짧게, 불릿은 가급적 한 줄, 브랜치 제목에 번호(`1.`)는 붙이지 않음

## 수동 편집 시 참고 (빌더 미사용)

템플릿 플레이스홀더:

| 플레이스홀더 | 내용 |
|--------------|------|
| `{{TITLE}}` | 페이지 제목 (h1과 `<title>` 공용) |
| `{{DESCRIPTION}}` | 제목 아래 한 줄 설명 |
| `{{SUBJECT}}` | 교과명 — 미정 시 속성 전체 삭제 |
| `{{MODE}}` | `교과용` / `발표용` / `퀴즈형` |
| `{{CENTER_TITLE}}` / `{{CENTER_TEXT}}` | 중앙 원의 제목 / 보조 설명 |
| `{{PEDAGOGY}}` | 선택 교육 설계 메타데이터 패널 — 없으면 빈 문자열 |
| `{{BRANCHES}}` | 브랜치 노드 마크업 (아래 패턴) |
| `{{HINT}}` | 하단 안내 (기본: "각 가지 카드를 클릭하면 자세한 내용이 열립니다.") |

브랜치 마크업 패턴 — `data-connect="left|right"`는 **좌/우 컬럼 배치용** 속성이다
(연결선은 중앙 외 모든 `.node`에 자동으로 그려지며 data-connect와 무관):

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

`branch-1`~`branch-8` 클래스가 카드 색을 결정. 단일 파일 산출물에서는 사용하지 않는
`[data-subject]` 테마 블록을 제거해도 된다 (빌더 산출물은 그대로 둠).

## 스타일·레이아웃 불변 규칙

- `DESIGN.md`의 classroom whiteboard workspace 방향과 토큰을 우선 적용
- `font-family: "Malgun Gothic", "맑은 고딕", sans-serif` / 주요 라벨 bold
- 글자 크기 위계: 페이지 제목 > 중앙 주제 > 브랜치 제목 > 불릿
- 저채도·저피로 색상 (네온·과채도·다크 테마는 요청 시에만), 텍스트 대비 확보
- `word-break: keep-all; overflow-wrap: anywhere; overflow-x: hidden;` — 한글 가독성과 모바일 넘침 방지를 함께 처리
- 연결선은 실제 노드 위치에서 계산 (하드코딩 금지) — 템플릿 JS가 리사이즈·펼침 시 자동 재계산
- 드래그앤드롭, 물리 모션, 자동재생 애니메이션, 타이머 퀴즈는 명시 요청 + 승인 없이는 금지
- 브랜드 클론 색상·로고·제품 chrome, bokeh/orbs, generic AI gradients, marketing hero 구성은 기본값으로 금지

## 품질 체크리스트

완료 전 전부 확인:

- [ ] 교과 테마 적용(또는 기본 테마) + 마지막에 한 줄 언급
- [ ] 모드가 `data-mode`에 반영됨
- [ ] 수업 목적이 렌더링 모드와 분리되어 정해짐
- [ ] 초점 질문·선수 지식·오개념·어휘 지원이 필요한 경우 `pedagogy`에 반영됨
- [ ] 브랜치 구조가 교과/수업 목적에 맞고 최대 8개를 넘지 않음
- [ ] 주제·위계(중앙 > 브랜치)가 정확
- [ ] `pedagogy`가 없을 때 빈 패널·빈 라벨이 생기지 않음
- [ ] 데스크톱 노드 겹침 없음 / 하단 노드 잘림 없음 / 연결선이 노드에 접함
- [ ] 한글 단어 중간 줄바꿈 없음 / 모바일 가독성 유지
- [ ] 애니메이션·퀴즈는 승인 후에만 추가됨
- [ ] 시각/템플릿 변경 시 `DESIGN.md`와 일치함
- [ ] 시각/템플릿 변경 시 실제 브라우저 visual QA를 1280px 이상, 768px, 375-390px, print, reduced motion, branch/quiz 상태에서 확인함

검증 방법: 가능하면 브라우저로 파일을 열어 데스크톱(1280px 이상)·태블릿(768px)·모바일(375-390px)
렌더링과 print/reduced-motion, branch expand/collapse, quiz answer open/closed 상태를 직접 확인.
브라우저 검증이 불가한 환경이면 코드 검토로 확인하되, 결과 보고 시
"렌더링 미검증"을 명시할 것.

코드 검토 시 주의: `data-connect` 문자열은 템플릿 내장 JS의 querySelector에도 2회 등장하므로,
브랜치 수는 `<div class="node branch-` 패턴으로 셀 것. 템플릿의 `requestAnimationFrame`은
연결선 재계산용 내장 코드이며 "자동재생 애니메이션"에 해당하지 않음.
