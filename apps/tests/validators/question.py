from ..constants.messages import QuestionMessages
from ..exceptions import AppValidationError


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
