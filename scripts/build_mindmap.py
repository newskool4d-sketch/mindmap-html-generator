# -*- coding: utf-8 -*-
"""JSON 스펙 → 마인드맵 HTML 자동 생성 빌더.

사용법:
    python build_mindmap.py spec.json [-o 출력폴더] [--template 템플릿경로]

JSON 스펙 형식 (UTF-8):
{
  "title": "페이지 제목",
  "description": "제목 아래 한 줄 설명",
  "subject": "정보",            // 선택. 지원 교과 외 값이면 경고 후 기본 테마
  "mode": "발표용",             // 선택. 교과용(기본) | 발표용 | 퀴즈형
  "center": {"title": "중심 주제", "text": "중심 보조 설명"},
  "branches": [
    {
      "title": "브랜치 제목",
      "sub": "짧은 부제",        // 선택
      "icon": "bi-robot",        // 선택. Bootstrap Icons 클래스
      "side": "left",            // 선택. left | right (생략 시 자동 배분)
      "details": ["불릿 1", "불릿 2"],
      "quiz": {"q": "질문", "a": "정답"}   // 선택. 퀴즈형 모드에서 사용
    }
  ],
  "hint": "하단 안내 문구",      // 선택. 생략 시 기본 문구
  "pedagogy": {                  // 선택. v3 교육 설계 메타데이터
    "grade_band": "middle 1-3",
    "audience_level": "introductory",
    "focus_question": "이 개념을 왜, 어떻게 연결해야 할까?",
    "lesson_purpose": "도입 | 정리 | 복습 | 평가 | 탐구",
    "achievement_standard_note": "사람이 작성한 참고 메모. 공식 매핑 자동 생성 아님.",
    "prior_knowledge": ["이미 알고 있어야 할 개념"],
    "misconceptions": ["오개념 또는 혼동 지점"],
    "vocabulary_support": ["핵심 어휘"],
    "transfer_generalization_prompt": "다른 상황에 적용해 볼 질문",
    "metacognitive_prompt": "내 이해를 점검하는 질문",
    "assessment_prompt_types": ["explanation", "misconception check", "transfer"]
  }
}

`pedagogy`는 모두 선택 필드이며, 없으면 기존 v2 출력은 변하지 않는다.
향후 렌더러는 값이 있을 때만 간결한 교사/학생 지원 패널을 표시할 수 있으며,
없는 필드 때문에 빈 라벨이나 빈 출력 영역을 만들지 않는다.
공식 교육과정 성취기준 매핑은 자동 생성하지 않는다.
퀴즈, 타이머, 점수, 게임, 애니메이션 동작은 계속 명시적 승인 후에만 사용한다.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SUPPORTED_SUBJECTS = [
    "국어", "수학", "과학", "사회", "영어", "미술", "음악",
    "체육", "역사", "도덕", "정보", "실과", "진로",
]
SUPPORTED_MODES = ["교과용", "발표용", "퀴즈형"]
MAX_BRANCHES = 8
DEFAULT_HINT = "각 가지 카드를 클릭하면 자세한 내용이 열립니다."
QUIZ_HINT = "각 가지 카드를 클릭해 내용을 확인하고, [정답 보기] 버튼으로 스스로 점검해 보세요."
PEDAGOGY_TEXT_FIELDS = {
    "grade_band": "학년군",
    "audience_level": "학습자 수준",
    "focus_question": "초점 질문",
    "lesson_purpose": "수업 목적",
    "achievement_standard_note": "성취기준 메모",
    "transfer_generalization_prompt": "전이 질문",
    "metacognitive_prompt": "메타인지 질문",
}
PEDAGOGY_LIST_FIELDS = {
    "prior_knowledge": "선수 지식",
    "misconceptions": "오개념 점검",
    "vocabulary_support": "어휘 지원",
    "assessment_prompt_types": "형성 확인 유형",
}


def esc(value):
    return html.escape(str(value), quote=True)


def build_pedagogy_html(pedagogy):
    if not pedagogy:
        return ""

    items = []
    for key, label in PEDAGOGY_TEXT_FIELDS.items():
        value = pedagogy.get(key)
        if isinstance(value, str) and value.strip():
            items.append(
                f"""<li class="pedagogy-item">
      <strong>{esc(label)}</strong>
      <span>{esc(value.strip())}</span>
    </li>"""
            )

    for key, label in PEDAGOGY_LIST_FIELDS.items():
        values = pedagogy.get(key)
        if isinstance(values, list):
            children = [item for item in values if isinstance(item, str) and item.strip()]
            if children:
                list_html = "\n".join(f"          <li>{esc(item.strip())}</li>" for item in children)
                items.append(
                    f"""<li class="pedagogy-item">
      <strong>{esc(label)}</strong>
      <ul class="pedagogy-list">
{list_html}
      </ul>
    </li>"""
                )

    if not items:
        return ""

    body = "\n    ".join(items)
    return f"""<aside class="pedagogy" aria-label="학습 지원 정보">
  <h2>학습 지원</h2>
  <ul class="pedagogy-grid">
    {body}
  </ul>
</aside>"""


def build_branch_html(branch, index, side):
    title = esc(branch["title"])
    icon = branch.get("icon", "").strip()
    icon_html = f'<i class="bi {esc(icon)}"></i> ' if icon else ""
    content_id = f"branch-{index}-content"
    sub_html = ""
    if branch.get("sub"):
        sub_html = f'\n    <div class="node-sub">{esc(branch["sub"])}</div>'

    details = "\n".join(f"      <li>{esc(item)}</li>" for item in branch.get("details", []))
    quiz_html = ""
    quiz = branch.get("quiz")
    if quiz:
        answer_id = f"branch-{index}-quiz-answer"
        quiz_html = f"""
    <div class="quiz">
      <p class="quiz-q"><i class="bi bi-question-circle"></i> {esc(quiz["q"])}</p>
      <button type="button" class="quiz-toggle" aria-controls="{answer_id}" data-label="{title}" aria-label="{title} 정답 보기">정답 보기</button>
      <p id="{answer_id}" class="quiz-a hidden" aria-hidden="true">{esc(quiz["a"])}</p>
    </div>"""

    return f"""<div class="node branch-{index}" data-connect="{side}">
  <button type="button" aria-controls="{content_id}" data-label="{title}" aria-label="{title} 자세히 보기">
    <div class="node-title">
      <span>{icon_html}{title}</span>
      <span class="icon" aria-hidden="true">+</span>
    </div>{sub_html}
  </button>
  <div id="{content_id}" class="content" role="region" aria-label="{title} 세부 내용" aria-hidden="true">
    <ul>
{details}
    </ul>{quiz_html}
  </div>
</div>"""


def assign_sides(branches):
    """side 미지정 브랜치를 좌/우 교대로 배분 (홀수면 왼쪽이 1개 더 많음)."""
    auto_toggle = 0
    sides = []
    for branch in branches:
        side = branch.get("side")
        if side not in ("left", "right"):
            side = "left" if auto_toggle % 2 == 0 else "right"
            auto_toggle += 1
        sides.append(side)
    return sides


def sanitize_filename(name):
    cleaned = re.sub(r'[\\/:*?"<>|]', "", name).strip()
    return re.sub(r"\s+", "_", cleaned) or "mindmap"


def validate_spec(spec):
    errors = []
    for key in ("title", "center", "branches"):
        if key not in spec:
            errors.append(f"필수 키 누락: {key}")
    if "center" in spec:
        for key in ("title", "text"):
            if key not in spec["center"]:
                errors.append(f"center.{key} 누락")
    branches = spec.get("branches", [])
    if not branches:
        errors.append("branches가 비어 있음")
    if len(branches) > MAX_BRANCHES:
        errors.append(f"브랜치 {len(branches)}개 — 최대 {MAX_BRANCHES}개 (인접 항목을 통합할 것)")
    for i, branch in enumerate(branches, 1):
        if "title" not in branch:
            errors.append(f"branches[{i}].title 누락")
        quiz = branch.get("quiz")
        if quiz and ("q" not in quiz or "a" not in quiz):
            errors.append(f"branches[{i}].quiz는 q와 a가 모두 필요")
    pedagogy = spec.get("pedagogy")
    if pedagogy is not None:
        if not isinstance(pedagogy, dict):
            errors.append("pedagogy는 객체여야 함")
        else:
            for key, label in PEDAGOGY_TEXT_FIELDS.items():
                if key in pedagogy and not isinstance(pedagogy[key], str):
                    errors.append(f"pedagogy.{key}({label})는 문자열이어야 함")
            for key, label in PEDAGOGY_LIST_FIELDS.items():
                value = pedagogy.get(key)
                if key in pedagogy and (
                    not isinstance(value, list)
                    or any(not isinstance(item, str) for item in value)
                ):
                    errors.append(f"pedagogy.{key}({label})는 문자열 목록이어야 함")
    mode = spec.get("mode", "교과용")
    if mode not in SUPPORTED_MODES:
        errors.append(f"mode '{mode}' 미지원 — {SUPPORTED_MODES} 중 선택")
    return errors


def build(spec_path, out_dir=None, template_path=None):
    spec_path = Path(spec_path)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    errors = validate_spec(spec)
    if errors:
        for err in errors:
            print(f"[오류] {err}")
        sys.exit(1)

    if template_path is None:
        template_path = Path(__file__).resolve().parent.parent / "assets" / "base-mindmap-template.html"
    template = Path(template_path).read_text(encoding="utf-8")

    mode = spec.get("mode", "교과용")
    subject = (spec.get("subject") or "").strip()
    if subject and subject not in SUPPORTED_SUBJECTS:
        print(f"[경고] 교과 '{subject}' 테마 미지원 — 기본 테마 적용 (지원: {', '.join(SUPPORTED_SUBJECTS)})")
        subject = ""

    branches = spec["branches"]
    sides = assign_sides(branches)
    if mode == "퀴즈형" and not any(b.get("quiz") for b in branches):
        print("[경고] 퀴즈형 모드인데 quiz 항목이 있는 브랜치가 없음")

    branch_html = "\n\n      ".join(
        build_branch_html(branch, i + 1, sides[i]) for i, branch in enumerate(branches)
    )
    pedagogy_html = build_pedagogy_html(spec.get("pedagogy"))

    default_hint = QUIZ_HINT if mode == "퀴즈형" else DEFAULT_HINT
    result = template
    if subject:
        result = result.replace('data-subject="{{SUBJECT}}"', f'data-subject="{esc(subject)}"')
    else:
        result = result.replace(' data-subject="{{SUBJECT}}"', "")
    result = (
        result
        .replace("{{MODE}}", esc(mode))
        .replace("{{TITLE}}", esc(spec["title"]))
        .replace("{{DESCRIPTION}}", esc(spec.get("description", "")))
        .replace("{{CENTER_TITLE}}", esc(spec["center"]["title"]))
        .replace("{{CENTER_TEXT}}", esc(spec["center"]["text"]))
        .replace("{{PEDAGOGY}}", pedagogy_html)
        .replace("{{BRANCHES}}", branch_html)
        .replace("{{HINT}}", esc(spec.get("hint", default_hint)))
    )

    out_dir = Path(out_dir) if out_dir else spec_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{sanitize_filename(spec['title'])}_{mode}.html"
    out_path.write_text(result, encoding="utf-8")

    left_count = sides.count("left")
    print(f"[완료] {out_path}")
    print(f"  모드: {mode} / 교과 테마: {subject or '기본(그린)'} / 브랜치: {len(branches)}개 (좌 {left_count}·우 {len(branches) - left_count})")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="JSON 스펙으로 마인드맵 HTML 생성")
    parser.add_argument("spec", help="JSON 스펙 파일 경로")
    parser.add_argument("-o", "--out-dir", default=None, help="출력 폴더 (기본: 스펙 파일 위치)")
    parser.add_argument("--template", default=None, help="템플릿 경로 (기본: 스킬 내장 템플릿)")
    args = parser.parse_args()
    build(args.spec, args.out_dir, args.template)


if __name__ == "__main__":
    main()
