from PIL import Image, UnidentifiedImageError

from ..constants.limits import QuestionLimits
from ..constants.messages import QuestionMessages
from ..exceptions import AppValidationError
from ..models.question import Question
from ..models.test import Test


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


def validate_question_limit(*, test: Test) -> None:
    if test.questions.count() >= QuestionLimits.MAX_QUESTIONS:
        raise AppValidationError([QuestionMessages.QUESTION_LIMIT])


def validate_question_image_size(
    *,
    image,
    max_size: int,
) -> None:
    if image.size > max_size:
        max_size_mb = max_size // (1024 * 1024)

        raise AppValidationError([
            f'Максимальный размер изображения {max_size_mb} МБ',
        ])


def validate_question_image_format(
    *,
    image,
    allowed_formats: set[str],
) -> None:
    image.seek(0)

    try:
        with Image.open(image) as pil_image:
            if pil_image.format not in allowed_formats:
                raise AppValidationError([
                    QuestionMessages.WRONG_IMAGE_FORMAT,
                ])
    except UnidentifiedImageError:
        raise AppValidationError([
            QuestionMessages.WRONG_IMAGE_FORMAT,
        ])
    finally:
        image.seek(0)


def validate_question_image_resolution(
    *,
    image,
    max_width: int,
    max_height: int,
) -> None:
    image.seek(0)

    try:
        with Image.open(image) as pil_image:
            width, height = pil_image.size

            if width > max_width or height > max_height:
                raise AppValidationError([
                    QuestionMessages.IMAGE_TOO_LARGE,
                ])
    except UnidentifiedImageError:
        raise AppValidationError([
            QuestionMessages.WRONG_IMAGE_FORMAT,
        ])
    finally:
        image.seek(0)


def validate_question_image(*, image) -> None:
    validate_question_image_size(
        image=image,
        max_size=QuestionLimits.MAX_IMAGE_SIZE,
    )

    validate_question_image_format(
        image=image,
        allowed_formats=QuestionLimits.ALLOWED_IMAGE_FORMATS,
    )

    validate_question_image_resolution(
        image=image,
        max_width=QuestionLimits.MAX_IMAGE_WIDTH,
        max_height=QuestionLimits.MAX_IMAGE_HEIGHT,
    )
