import pytest

from ..constants.limits import QuestionLimits
from ..exceptions import AppValidationError
from ..models.question import Question
from ..validators.question import validate_question_text, validate_question_type


class TestValidateQuestion:
    def test_empty_text(self):
        with pytest.raises(AppValidationError):
            validate_question_text(
                text='',
                max_length=QuestionLimits.TITLE_MAX_LENGTH,
            )

    def test_equal_max(self):
        text = 'a' * QuestionLimits.TITLE_MAX_LENGTH

        validate_question_text(
            text=text,
            max_length=QuestionLimits.TITLE_MAX_LENGTH,
        )

    def test_greater_than_max(self):
        text = 'a' * (QuestionLimits.TITLE_MAX_LENGTH + 1)

        with pytest.raises(AppValidationError):
            validate_question_text(
                text=text,
                max_length=QuestionLimits.TITLE_MAX_LENGTH,
            )


class TestValidateQuestionText:
    def test_empty_text(self):
        with pytest.raises(AppValidationError):
            validate_question_text(
                text='',
                max_length=QuestionLimits.TITLE_MAX_LENGTH,
            )

    def test_equal_max(self):
        text = 'a' * QuestionLimits.TITLE_MAX_LENGTH

        validate_question_text(
            text=text,
            max_length=QuestionLimits.TITLE_MAX_LENGTH,
        )

    def test_greater_than_max(self):
        text = 'a' * (QuestionLimits.TITLE_MAX_LENGTH + 1)

        with pytest.raises(AppValidationError):
            validate_question_text(
                text=text,
                max_length=QuestionLimits.TITLE_MAX_LENGTH,
            )


class TestValidateQuestionType:
    def test_empty_type(self):
        with pytest.raises(AppValidationError):
            validate_question_type(
                question_type='',
            )

    def test_wrong_type(self):
        with pytest.raises(AppValidationError):
            validate_question_type(
                question_type='false_type',
            )

    def test_valid_type(self):
        validate_question_type(
            question_type=Question.QuestionType.SINGLE_CHOICE,
        )
