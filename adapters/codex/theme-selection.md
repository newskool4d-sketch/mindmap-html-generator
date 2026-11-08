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
