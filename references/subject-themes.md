# Subject Themes

교과별 색상 테마와 Bootstrap Icons 아이콘 추천 목록.
CSS 변수는 `base-mindmap-template.html`의 `[data-subject]` 블록에 이미 정의되어 있음.

**중요**: `data-subject` 속성은 반드시 `<html>` 태그에 달 것.
`:root`(=html)에 정의된 기본 변수를 `html[data-subject]`가 덮어쓰는 구조이므로
body나 다른 요소에 달면 `--bg` 등 테마가 깨짐.

## Bootstrap Icons CDN

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" />
```

템플릿 head에 이미 포함됨. 별도 추가 불필요.

## 교과별 아이콘 추천

### 국어 (따뜻한 베이지/브라운)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-book` |
| 글쓰기/표현 | `bi-pencil` |
| 읽기/독해 | `bi-file-text` |
| 문법/언어 | `bi-spell-check` |
| 문학/작품 | `bi-journal-bookmark` |
| 말하기/듣기 | `bi-chat-square-text` |
| 핵심 정리 | `bi-bookmark-star` |

### 수학 (차분한 블루)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-calculator` |
| 공식/규칙 | `bi-function` |
| 도형/기하 | `bi-pentagon` |
| 수와 연산 | `bi-123` |
| 확률/통계 | `bi-bar-chart` |
| 문제 풀이 | `bi-pencil-square` |
| 핵심 정리 | `bi-check2-circle` |

### 과학 (신선한 그린)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-atom` |
| 실험/관찰 | `bi-eyedropper` |
| 생물/생명 | `bi-tree` |
| 물리/힘 | `bi-lightning` |
| 화학/물질 | `bi-droplet` |
| 지구/우주 | `bi-globe` |
| 핵심 정리 | `bi-star` |

### 사회 (따뜻한 오렌지)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-people` |
| 지리/환경 | `bi-map` |
| 경제/산업 | `bi-currency-dollar` |
| 정치/제도 | `bi-bank` |
| 문화/역사 | `bi-flag` |
| 사회 문제 | `bi-exclamation-circle` |
| 핵심 정리 | `bi-patch-check` |

### 영어 (부드러운 퍼플)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 어휘/단어 | `bi-translate` |
| 문법/구조 | `bi-type` |
| 읽기/독해 | `bi-file-earmark-text` |
| 말하기/회화 | `bi-mic` |
| 듣기/발음 | `bi-headphones` |
| 쓰기/작문 | `bi-pen` |
| 핵심 정리 | `bi-bookmark` |

### 미술 (화사한 핑크)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-palette` |
| 색채/배색 | `bi-droplet-half` |
| 조형/구성 | `bi-grid` |
| 감상/비평 | `bi-eye` |
| 표현 기법 | `bi-brush` |
| 작품/사례 | `bi-image` |
| 핵심 정리 | `bi-stars` |

### 음악 (차분한 바이올렛)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-music-note-beamed` |
| 리듬/박자 | `bi-soundwave` |
| 화음/화성 | `bi-music-note-list` |
| 악기/연주 | `bi-guitar` |
| 감상/비평 | `bi-ear` |
| 창작/작곡 | `bi-music-player` |
| 핵심 정리 | `bi-star-fill` |

### 체육 (활기찬 레드)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-trophy` |
| 운동 종목 | `bi-dribbble` |
| 건강/체력 | `bi-heart-pulse` |
| 규칙/방법 | `bi-list-check` |
| 안전/주의 | `bi-shield-check` |
| 연습/훈련 | `bi-arrow-repeat` |
| 핵심 정리 | `bi-award` |

### 역사 (고풍스러운 세피아)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-clock-history` |
| 시대/시기 | `bi-calendar3` |
| 인물/사건 | `bi-person-badge` |
| 배경/원인 | `bi-diagram-3` |
| 결과/영향 | `bi-arrow-right-circle` |
| 유물/문화재 | `bi-archive` |
| 핵심 정리 | `bi-bookmark-fill` |

### 도덕 (자연스러운 민트그린)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-heart` |
| 가치/덕목 | `bi-gem` |
| 사례/상황 | `bi-chat-dots` |
| 판단/기준 | `bi-scale` |
| 실천/행동 | `bi-hand-thumbs-up` |
| 성찰/반성 | `bi-journal-text` |
| 핵심 정리 | `bi-check-circle` |

### 정보 (테크 틸)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-cpu` |
| 인공지능/AI | `bi-robot` |
| 데이터/정보 | `bi-database` |
| 코딩/프로그래밍 | `bi-code-slash` |
| 알고리즘/원리 | `bi-gear` |
| 네트워크/인터넷 | `bi-globe2` |
| 정보 윤리/보안 | `bi-shield-lock` |
| 핵심 정리 | `bi-check2-square` |

### 실과 (올리브 그린)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-tools` |
| 기술/만들기 | `bi-wrench` |
| 가정/생활 | `bi-house-heart` |
| 식생활/요리 | `bi-egg-fried` |
| 의생활/소비 | `bi-bag` |
| 농업/생명 | `bi-flower1` |
| 핵심 정리 | `bi-clipboard-check` |

### 진로 (웜 골드)
| 브랜치 유형 | 아이콘 클래스 |
|------------|--------------|
| 개념/정의 | `bi-signpost-split` |
| 자기 이해 | `bi-person-heart` |
| 직업 세계 | `bi-briefcase` |
| 진로 탐색 | `bi-search` |
| 진로 설계 | `bi-map` |
| 역량/준비 | `bi-mortarboard` |
| 핵심 정리 | `bi-flag-fill` |

## 사용 예시

```html
<div class="node-title">
  <span><i class="bi bi-atom"></i> 광합성 개념</span>
  <span class="icon">+</span>
</div>
```

## 주의사항

- 아이콘은 라벨 앞에 `<i>` 태그로 삽입
- 별도 크기·색상 지정 없이 기본 상태 사용 (테마 색과 자동 조화)
- 브랜치 내용과 의미가 맞는 아이콘만 사용, 억지로 끼워 넣지 않을 것
- 인터넷 연결 없는 환경에서는 CDN 불러오기 실패 → 아이콘 대신 빈칸으로 처리됨 (레이아웃 깨지지 않음)
