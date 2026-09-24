import pytest

from ..exceptions import AppValidationError
from ..validators.answer import validate_answer_text, validate_answer_limit, validate_answer_exists
from ..constants.limits import AnswerLimits


class TestValidateAnswerText:
    def test_empty_text(self):
        with pytest.raises(AppValidationError):
            validate_answer_text(
                text='',
                max_length=AnswerLimits.MAX_TITLE_LENGTH,
            )

    def test_equal_max(self):
        text = 'a' * AnswerLimits.MAX_TITLE_LENGTH

        validate_answer_text(
            text=text,
            max_length=AnswerLimits.MAX_TITLE_LENGTH,
        )

    def test_greater_than_max(self):
        text = 'a' * (AnswerLimits.MAX_TITLE_LENGTH + 1)

        with pytest.raises(AppValidationError):
            validate_answer_text(
                text=text,
                max_length=AnswerLimits.MAX_TITLE_LENGTH,
            )


@pytest.mark.django_db
class TestValidateAnswerLimit:
    def test_limit_not_reached(self, question):
        validate_answer_limit(
            question=question,
        )

    def test_limit_reached(self, question, answer_factory):
        for i in range(AnswerLimits.MAX_ANSWERS):
            answer_factory(question=question)

        with pytest.raises(AppValidationError):
            validate_answer_limit(
                question=question,
            )


@pytest.mark.django_db
class TestValidateAnswerExists:
    def test_answer_does_not_exist(self, question):
        validate_answer_exists(
            question=question,
            text='True answer',
        )

    def test_answer_exists(self, question, answer):
        with pytest.raises(AppValidationError):
            validate_answer_exists(
                question=question,
                text=answer.text,
            )
