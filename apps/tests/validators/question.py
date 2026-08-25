from ..constants.messages import QuestionMessages
from ..exceptions import AppValidationError
from ..models.question import Question


def validate_question_text(
    *,
    text: str,
    max_length: int,
) -> None:
    text = text.strip()

    if not text:
        raise AppValidationError([QuestionMessages.EMPTY_TEXT])

    if len(text) > max_length:
        raise AppValidationError([
            f'Максимальная длина {max_length} символов',
        ])


def validate_question_type(*, question_type: str) -> None:
    if not question_type:
        raise AppValidationError([QuestionMessages.TYPE_NOT_FOUND])

    if question_type not in Question.QuestionType.values:
        raise AppValidationError([QuestionMessages.WRONG_TYPE])
