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
  "hint": "하단 안내 문구"       // 선택. 생략 시 기본 문구
}
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


def esc(value):
    return html.escape(str(value), quote=True)


def build_branch_html(branch, index, side):
    title = esc(branch["title"])
    icon = branch.get("icon", "").strip()
    icon_html = f'<i class="bi {esc(icon)}"></i> ' if icon else ""
    sub_html = ""
    if branch.get("sub"):
        sub_html = f'\n    <div class="node-sub">{esc(branch["sub"])}</div>'

    details = "\n".join(f"      <li>{esc(item)}</li>" for item in branch.get("details", []))
    quiz_html = ""
    quiz = branch.get("quiz")
    if quiz:
        quiz_html = f"""
    <div class="quiz">
      <p class="quiz-q"><i class="bi bi-question-circle"></i> {esc(quiz["q"])}</p>
      <button type="button" class="quiz-toggle">정답 보기</button>
      <p class="quiz-a hidden">{esc(quiz["a"])}</p>
    </div>"""

    return f"""<div class="node branch-{index}" data-connect="{side}">
  <button type="button">
    <div class="node-title">
      <span>{icon_html}{title}</span>
      <span class="icon">+</span>
    </div>{sub_html}
  </button>
  <div class="content">
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
