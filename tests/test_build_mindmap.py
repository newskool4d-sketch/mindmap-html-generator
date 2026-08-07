from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILDER = REPO_ROOT / "scripts" / "build_mindmap.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures"
SCRATCH_OUT = REPO_ROOT / "tests" / ".out"


@dataclass(frozen=True, slots=True)
class BuilderRun:
    returncode: int
    stdout: str
    stderr: str


def run_builder(fixture_name: str, out_dir: Path) -> BuilderRun:
    completed = subprocess.run(
        [sys.executable, str(BUILDER), str(FIXTURES / fixture_name), "-o", str(out_dir)],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=15,
    )
    return BuilderRun(completed.returncode, completed.stdout, completed.stderr)


class BuildMindmapCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        SCRATCH_OUT.mkdir(parents=True, exist_ok=True)

    def test_current_v2_spec_generates_expected_html_markers(self) -> None:
        out_dir = SCRATCH_OUT / "current-v2-valid"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("current-v2-valid.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html_path = out_dir / "물의_순환_교과용.html"
        html = html_path.read_text(encoding="utf-8")
        self.assertIn('<html lang="ko" data-subject="과학" data-mode="교과용">', html)
        self.assertIn("물의 순환", html)
        self.assertEqual(html.count('<div class="node branch-'), 4)
        self.assertEqual(html.count('<div class="node branch-1" data-connect="left">'), 1)
        self.assertEqual(html.count('<div class="node branch-2" data-connect="right">'), 1)
        self.assertEqual(html.count('<div class="node branch-3" data-connect="left">'), 1)
        self.assertEqual(html.count('<div class="node branch-4" data-connect="right">'), 1)
        self.assertNotIn("{{", html)
        self.assertNotIn('<aside class="pedagogy"', html)
        self.assertIn("[완료]", result.stdout)

    def test_unsupported_subject_falls_back_to_default_theme(self) -> None:
        out_dir = SCRATCH_OUT / "unsupported-subject-fallback"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("unsupported-subject-fallback.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html_path = out_dir / "생활_속_선택_발표용.html"
        html = html_path.read_text(encoding="utf-8")
        html_tag = html.splitlines()[1]
        self.assertIn("[경고] 교과 '철학' 테마 미지원", result.stdout)
        self.assertIn('data-mode="발표용"', html_tag)
        self.assertNotIn("data-subject=", html_tag)
        self.assertNotIn("{{", html)

    def test_invalid_too_many_branches_exits_nonzero_with_korean_error(self) -> None:
        result = run_builder("invalid-too-many-branches.json", SCRATCH_OUT / "invalid-too-many")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[오류] 브랜치 9개 — 최대 8개", result.stdout)

    def test_invalid_quiz_requires_question_and_answer(self) -> None:
        result = run_builder("invalid-quiz-qa.json", SCRATCH_OUT / "invalid-quiz-qa")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[오류] branches[1].quiz는 q와 a가 모두 필요", result.stdout)

    def test_invalid_mode_lists_supported_modes(self) -> None:
        result = run_builder("invalid-mode-validation.json", SCRATCH_OUT / "invalid-mode")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[오류] mode '토론용' 미지원", result.stdout)
        self.assertIn("교과용", result.stdout)
        self.assertIn("발표용", result.stdout)
        self.assertIn("퀴즈형", result.stdout)

    def test_v3_pedagogy_spec_renders_optional_support_panel(self) -> None:
        out_dir = SCRATCH_OUT / "v3-pedagogy"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("v3-pedagogy.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html_path = out_dir / "구름과_물의_순환_교과용.html"
        html = html_path.read_text(encoding="utf-8")
        self.assertIn('<html lang="ko" data-subject="과학" data-mode="교과용">', html)
        self.assertEqual(html.count('<div class="node branch-'), 3)
        self.assertEqual(html.count('<div class="node branch-1" data-connect="left">'), 1)
        self.assertEqual(html.count('<div class="node branch-2" data-connect="right">'), 1)
        self.assertEqual(html.count('<div class="node branch-3" data-connect="left">'), 1)
        self.assertIn('<aside class="pedagogy" aria-label="학습 지원 정보">', html)
        self.assertIn("초점 질문", html)
        self.assertIn("오개념 점검", html)
        self.assertIn("어휘 지원", html)
        self.assertIn("전이 질문", html)
        self.assertIn("형성 확인 유형", html)
        self.assertIn("&lt;구름&gt;", html)
        self.assertNotIn("{{", html)

    def test_single_field_pedagogy_renders_only_that_item(self) -> None:
        out_dir = SCRATCH_OUT / "pedagogy-single-field"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("pedagogy-single-field.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html = (out_dir / "분수의_덧셈_교과용.html").read_text(encoding="utf-8")
        self.assertIn('<aside class="pedagogy" aria-label="학습 지원 정보">', html)
        self.assertEqual(html.count('<li class="pedagogy-item">'), 1)
        self.assertIn("초점 질문", html)
        for absent_label in ("학년군", "선수 지식", "오개념 점검", "어휘 지원", "형성 확인 유형"):
            self.assertNotIn(absent_label, html)
        self.assertNotIn("{{", html)

    def test_quiz_block_renders_only_for_branches_with_quiz_data(self) -> None:
        out_dir = SCRATCH_OUT / "quiz-approved"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("quiz-approved.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        html_path = out_dir / "알고리즘_점검_퀴즈형.html"
        html = html_path.read_text(encoding="utf-8")
        self.assertIn('data-mode="퀴즈형"', html)
        self.assertEqual(html.count('<div class="quiz">'), 1)
        self.assertEqual(html.count('class="quiz-toggle"'), 1)
        self.assertIn("&lt;입력&gt;은 무엇을 뜻하나요?", html)
        self.assertIn("문제 해결에 필요한 값을 받는 단계입니다.", html)
        self.assertIn('aria-label="입력 정답 보기"', html)
        self.assertNotIn("{{", html)

    def test_quiz_mode_without_quiz_data_does_not_create_quiz_block(self) -> None:
        out_dir = SCRATCH_OUT / "quiz-mode-no-quiz"
        if out_dir.exists():
            shutil.rmtree(out_dir)

        result = run_builder("quiz-mode-no-quiz.json", out_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[경고] 퀴즈형 모드인데 quiz 항목이 있는 브랜치가 없음", result.stdout)
        html_path = out_dir / "퀴즈_모드_안내_퀴즈형.html"
        html = html_path.read_text(encoding="utf-8")
        self.assertIn('data-mode="퀴즈형"', html)
        self.assertNotIn('<div class="quiz">', html)
        self.assertNotIn('class="quiz-toggle"', html)
        self.assertNotIn("{{", html)

    def test_invalid_pedagogy_type_exits_nonzero_with_korean_error(self) -> None:
        result = run_builder("invalid-pedagogy-type.json", SCRATCH_OUT / "invalid-pedagogy")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[오류] pedagogy는 객체여야 함", result.stdout)


import importlib.util


def _load_builder_module():
    module_spec = importlib.util.spec_from_file_location("build_mindmap", BUILDER)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


class BuilderUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bm = _load_builder_module()
        cls.template = (REPO_ROOT / "assets" / "base-mindmap-template.html").read_text(encoding="utf-8")

    def test_render_html_returns_html_and_meta_without_io(self) -> None:
        spec = {
            "title": "테스트 주제",
            "mode": "퀴즈형",
            "center": {"title": "중심", "text": "설명"},
            "branches": [{"title": "가지", "details": ["항목"]}],
        }
        html_text, meta = self.bm.render_html(spec, self.template)
        self.assertNotIn("{{", html_text)
        self.assertIn('data-mode="퀴즈형"', html_text)
        self.assertEqual(meta["mode"], "퀴즈형")
        self.assertEqual(meta["sides"], ["left"])
        self.assertEqual(meta["warnings"], ["퀴즈형 모드인데 quiz 항목이 있는 브랜치가 없음"])

    def test_render_html_unsupported_subject_falls_back_with_warning(self) -> None:
        spec = {
            "title": "테스트",
            "subject": "철학",
            "center": {"title": "중심", "text": "설명"},
            "branches": [{"title": "가지"}],
        }
        html_text, meta = self.bm.render_html(spec, self.template)
        self.assertEqual(meta["subject"], "")
        self.assertNotIn("data-subject=", html_text.splitlines()[1])
        self.assertIn("교과 '철학' 테마 미지원", meta["warnings"][0])

    def test_build_raises_spec_error_with_korean_messages(self) -> None:
        SCRATCH_OUT.mkdir(parents=True, exist_ok=True)
        bad = SCRATCH_OUT / "bad-spec.json"
        bad.write_text('{"title": "x"}', encoding="utf-8")
        with self.assertRaises(self.bm.SpecError) as ctx:
            self.bm.build(bad, SCRATCH_OUT / "bad-out")
        self.assertIn("필수 키 누락: center", ctx.exception.errors)
        self.assertIn("필수 키 누락: branches", ctx.exception.errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
