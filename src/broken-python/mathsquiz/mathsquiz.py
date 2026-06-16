"""A small command-line times-tables quiz.

Consolidated, object-oriented rewrite of the original broken ``mathsquiz.py``.
The legacy step files (``mathsquiz-step1.py`` .. ``mathsquiz-step3.py``) are
superseded by this single :class:`MathQuiz` class; see
``reports/mathsquiz_step_analysis.md`` for the evolution trail.

The original script shipped with six bugs (Python-2 ``print`` statements, ``=``
used for comparison, ``else if`` instead of ``elif``, a score that never
incremented, every question mislabelled "Question 1", and wrong expected
answers). All are fixed here, and the ten questions now run cleanly to a
maximum score of 10.
"""


class MathQuiz:
    """A ten-question multiplication quiz that tracks the player's score."""

    # Each question is a (first, second) pair; the correct answer is the
    # product, so the answers can never drift out of sync with the prompt.
    QUESTIONS = [
        (8, 7),
        (4, 9),
        (12, 6),
        (6, 8),
        (7, 7),
        (11, 6),
        (9, 2),
        (7, 9),
        (6, 6),
        (4, 8),
    ]

    def __init__(self, questions=None):
        self.questions = list(questions) if questions is not None else list(self.QUESTIONS)
        self.score = 0

    @staticmethod
    def check_answer(question, answer):
        """Return ``True`` if ``answer`` equals the product of ``question``.

        ``answer`` may be a string (as returned by :func:`input`) or an int.
        Non-numeric input counts as wrong rather than raising.
        """
        first, second = question
        try:
            return int(answer) == first * second
        except (TypeError, ValueError):
            return False

    def ask_question(self, number, question):
        """Pose one question to the player and update the score in place."""
        first, second = question
        print(f"Question {number}:")
        print(f"What is {first} x {second}?")
        answer = input("Answer: ")
        if self.check_answer(question, answer):
            print("Correct!")
            self.score += 1
        else:
            print("Wrong!")

    def run(self):
        """Ask every question in order, then show the result; return the score."""
        print("Hello! I'm going to ask you 10 maths questions.")
        print("Let's see how many you can get right!")
        self.score = 0
        for number, question in enumerate(self.questions, start=1):
            self.ask_question(number, question)
        self.display_result()
        return self.score

    def display_result(self):
        """Print the closing message based on the final score."""
        total = len(self.questions)
        print("That's all the questions done. So...what was your score...?")
        print(f"You scored {self.score} points out of a possible {total}.")
        if self.score < 5:
            print("You need to practice your maths!")
        elif self.score < 8:
            print("That's pretty good!")
        elif self.score < total:
            print("You did really well! Try and get 10 out of 10 next time!")
        else:
            print("Wow! What a maths star you are!! I'm impressed!")


if __name__ == "__main__":
    MathQuiz().run()
