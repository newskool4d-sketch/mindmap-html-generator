# design-next 수동 검수

QA 실행: `node tests/visual-qa.mjs --sample-dir .omo/evidence/design-next/out` — 4 샘플 · 28개 체크 · 실패 0 (PASS).
스크린샷 원본: `.omo/evidence/design-next/screenshots/2026-08-07T14-28-17-640Z/` (git 추적 제외, 로컬 확인용).

- **데스크톱 1280px**: `01-_-_-1280x900-rest.png` (물의_순환_교과용.html, 과학 테마) — 4개 브랜치 노트(증발·응결·강수·흐름)가 좌 2·우 2로 겹침·잘림 없이 배치, SVG 커넥터가 각 노트 좌우 모서리에 정확히 맞물림(Task 8에서 수정된 10px 오정렬 재발 없음), 노트 상단에 회전된 테이프 조각과 화이트보드 프레임(흰색 둥근 카드 + 그림자)이 렌더링됨, 중심 원은 초록 그라디언트로 텍스트 대비 양호. 노트 4색(분홍·주황·황토·연두) 구분 확인 — 이 샘플은 브랜치 4개뿐이라 6색 미만이며, 6색 이상 확인은 아래 8브랜치 샘플로 별도 수행.
- **모바일 390px**: `01-_-_-390x1200-rest.png` — 세로 스택 레이아웃, 가로 스크롤 없음(모든 카드가 뷰포트 폭 내 정렬), 데스크톱 전용 기울기(tilt) 미적용(카드 변이 없이 정직한 사각형). **버그 발견 및 수정**: 최초 렌더링에서 태블릿/모바일 브레이크포인트(`@media (max-width:1200px)`)가 `.node, .center`에 `position: static`을 적용해 테이프(`::after`, `position:absolute`)의 앵커 기준(positioning context)이 깨짐 → 노트별 테이프 4개가 모두 `.map` 기준 동일 좌표로 겹쳐 보이는 테이프 1개로 뭉쳐 보이는 결함을 확인. `assets/base-mindmap-template.html`의 해당 규칙을 `position: relative`로 변경했더니 이번엔 `.center`가 데스크톱 전용 `left:50%; top:50%`(absolute 중심정렬용)를 그대로 물려받아 오른쪽으로 밀려나는 2차 회귀 발생 → `top: 0; left: 0`을 명시적으로 리셋해 최종 수정. 재검증 결과 노트 4개 각각 독립된 테이프가 정상 위치에 렌더링됨(본 스크린샷에 반영됨).
- **퀴즈 열림**: `03-_-_-_-1280x900-quiz-open.png` (상태_점검_쇼케이스_퀴즈형.html, 정보 테마, 퀴즈형 모드) — "예시" 브랜치를 펼친 뒤 [정답 보기]를 눌러 퀴즈 패널 확장. 질문("이 브랜치의 상태는 무엇으로 점검하나요?")과 정답 텍스트("정답 보기 버튼의 열림·닫힘 상태로 점검합니다.")가 흰 배경에 짙은 텍스트로 대비 충분히 노출됨, 버튼 라벨이 "정답 닫기"로 토글되어 열림 상태 표시. 잘리거나 가려진 텍스트 없음.
- **print**: `01-_-_-1280x900-print.png` — 4개 브랜치 콘텐츠가 모두 펼쳐진 상태로 출력(접힘 없음), 커넥터 선(`.lines`)·아이콘(`.icon`)·힌트(`.hint`)·퀴즈 토글(`.quiz-toggle`) 모두 숨김 확인, 노트의 테이프·그림자·기울기(스큐어모피즘)가 인쇄용으로 평면화되어 사라짐(순수 색상 블록만 남음). **버그 발견 및 수정**: 최초 렌더링에서 print 미디어쿼리의 `.node { background-image: none; }` 규칙이 `class="node center"`를 공유하는 중심 원에도 적용되어 중심 원 고유 그라디언트 배경(`background: linear-gradient(...)`)까지 제거됨 → 흰 배경 위 흰 글자로 중심 제목("물의 순환")이 인쇄 시 사실상 안 보이는 결함 확인. 규칙을 `.node:not(.center) { background-image: none; }`로 좁혀 중심 원의 그라디언트 배경을 보존하도록 수정. 재검증 결과 중심 원 그라디언트와 흰 글자 대비가 정상 복원됨(본 스크린샷에 반영됨).
- **교과 테마 1종(정보, 퀴즈형 8브랜치 쇼케이스)**: `03-_-_-_-1280x900-rest.png` — 정의(분홍/로즈) · 분류(주황/피치) · 규칙(황토/옐로) · 예시(연두/그린) · 한계(민트/청록) · 적용(블루) · 비교(라벤더/퍼플) · 정리(핑크/마젠타) 8개 노트에서 서로 다른 8개 색조를 육안으로 구분(6계열 이상 충족), 특정 단색조로 무너지지 않음. 노트마다 개별 테이프·모서리 그림자 정상 렌더링, 겹침·잘림 없음.

## 수정 요약 (본 Task 중 발견)
- `assets/base-mindmap-template.html` `@media (max-width: 1200px)` 블록: `.node, .center { position: static; ... }` → `position: relative; top: 0; left: 0;` (모바일/태블릿 테이프 앵커 정상화, 중심 원 오프셋 회귀 방지)
- `assets/base-mindmap-template.html` `@media print` 블록: `.node { ...; background-image: none; }` → `.node:not(.center) { ...; background-image: none; }` (인쇄 시 중심 원 그라디언트 보존)
- 두 수정 모두 자동 QA 체크(overlap/overflow/placeholder/focus/print-content)에는 걸리지 않았고, 본 수동 스크린샷 검수로만 발견됨 — DESIGN.md 토큰 값은 변경하지 않고 기존 CSS 변수·선택자 범위 내에서 수정.
