"""Unit tests for the consolidated Math Quiz system (Phase 5).

Targets src/broken-python/mathsquiz/mathsquiz.py after Subagent Beta
consolidation. Covers: init, answer validation, answer correctness,
score increments, and result display messages.
"""

import sys
from pathlib import Path
from unittest.mock import patch

_MATHSQUIZ_DIR = (
    Path(__file__).resolve().parents[1] / "src" / "broken-python" / "mathsquiz"
)
sys.path.insert(0, str(_MATHSQUIZ_DIR))

from mathsquiz import MathQuiz  # noqa: E402


# ---------------------------------------------------------------------------
# Instantiation
# ---------------------------------------------------------------------------


class TestMathQuizInit:
    """Test MathQuiz class instantiation."""

    def test_initial_score_is_zero(self):
        assert MathQuiz().score == 0

    def test_questions_list_not_empty(self):
        assert len(MathQuiz().questions) > 0

    def test_ten_questions_loaded(self):
        """Assignment expects exactly 10 questions."""
        assert len(MathQuiz().questions) == 10

    def test_custom_questions_accepted(self):
        """Constructor accepts an explicit question list."""
        custom = [(2, 3), (4, 5)]
        quiz = MathQuiz(questions=custom)
        assert quiz.questions == custom


# ---------------------------------------------------------------------------
# Answer checking (static — no I/O)
# ---------------------------------------------------------------------------


class TestMathQuizAnswerValidation:
    """Test correct answer checking via check_answer."""

    def test_correct_int_answer(self):
        assert MathQuiz.check_answer((8, 7), 56) is True

    def test_correct_string_answer(self):
        """Input from the terminal arrives as a string."""
        assert MathQuiz.check_answer((8, 7), "56") is True

    def test_wrong_answer_returns_false(self):
        assert MathQuiz.check_answer((8, 7), 55) is False

    def test_non_numeric_answer_returns_false(self):
        """Regression: non-numeric input must not raise."""
        assert MathQuiz.check_answer((8, 7), "abc") is False

    def test_answer_uses_equality_not_assignment(self):
        """Regression: original used '=' instead of '=='."""
        # check_answer is a pure function — calling it must never raise
        result = MathQuiz.check_answer((4, 9), 36)
        assert result is True

    def test_correct_answer_increments_score(self):
        quiz = MathQuiz()
        with patch("builtins.input", return_value="56"):
            quiz.ask_question(1, (8, 7))
        assert quiz.score == 1

    def test_wrong_answer_does_not_increment_score(self):
        quiz = MathQuiz()
        with patch("builtins.input", return_value="55"):
            quiz.ask_question(1, (8, 7))
        assert quiz.score == 0


# ---------------------------------------------------------------------------
# Regression: correct expected answers (all were wrong in the original)
# ---------------------------------------------------------------------------


class TestMathQuizAnswerCorrectness:
    """Verify every default question has the right product."""

    def test_8_times_7_equals_56(self):
        """Original expected 55."""
        assert MathQuiz.check_answer((8, 7), 56) is True

    def test_4_times_9_equals_36(self):
        """Original expected 49."""
        assert MathQuiz.check_answer((4, 9), 36) is True

    def test_12_times_6_equals_72(self):
        """Original expected 126."""
        assert MathQuiz.check_answer((12, 6), 72) is True

    def test_6_times_8_equals_48(self):
        """Original expected 668."""
        assert MathQuiz.check_answer((6, 8), 48) is True

    def test_7_times_7_equals_49(self):
        """Original expected 77."""
        assert MathQuiz.check_answer((7, 7), 49) is True

    def test_11_times_6_equals_66(self):
        """Original expected 60."""
        assert MathQuiz.check_answer((11, 6), 66) is True


# ---------------------------------------------------------------------------
# Result display messages
# ---------------------------------------------------------------------------


class TestMathQuizResult:
    """Test display_result output for each score band."""

    def test_low_score_message(self, capsys):
        quiz = MathQuiz()
        quiz.score = 3
        quiz.display_result()
        assert "practice" in capsys.readouterr().out.lower()

    def test_medium_score_message(self, capsys):
        quiz = MathQuiz()
        quiz.score = 6
        quiz.display_result()
        assert "pretty good" in capsys.readouterr().out.lower()

    def test_high_score_message(self, capsys):
        """score 8–9 → 'really well'."""
        quiz = MathQuiz()
        quiz.score = 8
        quiz.display_result()
        assert "really well" in capsys.readouterr().out.lower()

    def test_perfect_score_message(self, capsys):
        quiz = MathQuiz()
        quiz.score = 10
        quiz.display_result()
        assert "maths star" in capsys.readouterr().out.lower()
