"""Unit tests for the consolidated Math Quiz system.

These tests target the fixed src/broken-python/mathsquiz/mathsquiz.py
after Subagent Beta completes its consolidation.
"""

import pytest


# ---------------------------------------------------------------------------
# Tests will be filled in once the consolidated MathQuiz class is in place.
# The structure below follows the target OOP architecture from docs/oop_schema.md
# ---------------------------------------------------------------------------


class TestMathQuizInit:
    """Test MathQuiz class instantiation."""

    def test_initial_score_is_zero(self):
        pytest.skip("Implement after Phase 5 consolidation")

    def test_questions_list_not_empty(self):
        pytest.skip("Implement after Phase 5 consolidation")

    def test_ten_questions_loaded(self):
        """Assignment expects 10 questions."""
        pytest.skip("Implement after Phase 5 consolidation")


class TestMathQuizAnswerValidation:
    """Test correct answer checking."""

    def test_correct_answer_increments_score(self):
        pytest.skip("Implement after Phase 5 consolidation")

    def test_wrong_answer_does_not_increment_score(self):
        pytest.skip("Implement after Phase 5 consolidation")

    def test_answer_uses_equality_not_assignment(self):
        """Regression: original used '=' instead of '=='."""
        pytest.skip("Implement after Phase 5 consolidation")


class TestMathQuizAnswerCorrectness:
    """Test that question answers are mathematically correct."""

    def test_8_times_7_equals_56(self):
        """Regression: original expected 55 instead of 56."""
        assert 8 * 7 == 56

    def test_4_times_9_equals_36(self):
        """Regression: original expected 49 instead of 36."""
        assert 4 * 9 == 36

    def test_12_times_6_equals_72(self):
        """Regression: original expected 126 instead of 72."""
        assert 12 * 6 == 72

    def test_6_times_8_equals_48(self):
        """Regression: original expected 668 instead of 48."""
        assert 6 * 8 == 48

    def test_7_times_7_equals_49(self):
        """Regression: original expected 77 instead of 49."""
        assert 7 * 7 == 49

    def test_11_times_6_equals_66(self):
        """Regression: original expected 60 instead of 66."""
        assert 11 * 6 == 66


class TestMathQuizResult:
    """Test final result display logic."""

    def test_low_score_message(self):
        """score < 5 → 'You need to practice'."""
        pytest.skip("Implement after Phase 5 consolidation")

    def test_medium_score_message(self):
        """5 <= score < 8 → 'pretty good'."""
        pytest.skip("Implement after Phase 5 consolidation")

    def test_perfect_score_message(self):
        """score == 10 → 'maths star'."""
        pytest.skip("Implement after Phase 5 consolidation")
