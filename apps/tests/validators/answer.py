from typing import Any

from ..constants.limits import AnswerLimits
from ..constants.messages import AnswerMessages
from ..exceptions import AppValidationError
from ..models.question import Question


def validate_answer_text(
    *,
    text: str,
    max_length: int,
) -> None:
    if not text:
        raise AppValidationError([AnswerMessages.EMPTY_TEXT])

    if len(text) > max_length:
        raise AppValidationError([
            f'Максимальная длина {max_length} символов',
        ])


def validate_answer_limit(*, question: Question) -> None:
    if question.answers.count() >= AnswerLimits.MAX_ANSWERS:
        raise AppValidationError([AnswerMessages.ANSWER_LIMIT])


def validate_answer_exists(
    *,
    question: Question,
    text: str,
) -> None:
    if question.answers.filter(text=text).exists():
        raise AppValidationError([AnswerMessages.ALREADY_EXISTS])


def validate_answers(
    *,
    questions: list[Question],
    answers: dict[str, Any],
) -> dict[str, Any]:
    question_ids = {str(question.id) for question in questions}

    if answers.keys() != question_ids:
        raise AppValidationError([AnswerMessages.WRONG_ID])

    validated = {}

    for question in questions:
        question_id = str(question.id)
        value = answers[question_id]

        if question.type == Question.QuestionType.SINGLE_CHOICE:
            validated[question_id] = int(value)

        elif question.type == Question.QuestionType.MULTIPLE_CHOICES:
            validated[question_id] = [
                int(answer_id)
                for answer_id in value
            ]

        elif question.type == Question.QuestionType.TEXT_FIELD:
            validated[question_id] = value.strip()

        else:
            raise AppValidationError([AnswerMessages.WRONG_TYPE])

    return validated
