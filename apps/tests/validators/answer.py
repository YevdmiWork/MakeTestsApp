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
