from django.core.exceptions import ValidationError

from .question import validate_question_for_publish, validate_question_text, validate_question_type
from ..constants.limits import TestLimits, QuestionLimits
from ..constants.messages import TestMessages
from ..exceptions import AppValidationError, PublishValidationError
from ..models.test import Test

from apps.users.models import User


def validate_test_limit(*, user: User) -> None:
    if Test.objects.filter(author=user).count() >= TestLimits.MAX_TESTS_FOR_USER:
        raise AppValidationError([TestMessages.TEST_LIMIT])


def validate_test(*, test: Test) -> None:
    try:
        test.full_clean()
    except ValidationError as e:
        raise AppValidationError(e.messages)


def validate_test_title(*, title: str | None) -> None:
    if title is None:
        return

    title = title.strip()
    title_length = len(title)

    if title_length < TestLimits.TITLE_MIN_LENGTH:
        raise AppValidationError([
            f'Название меньше {TestLimits.TITLE_MIN_LENGTH} символов'
        ])

    if title_length > TestLimits.TITLE_MAX_LENGTH:
        raise AppValidationError([
            f'Название больше {TestLimits.TITLE_MAX_LENGTH} символов'
        ])


def validate_test_content(*, content: str | None) -> None:
    if not content:
        return

    content = content.strip()
    content_length = len(content)

    if content_length > TestLimits.CONTENT_MAX_LENGTH:
        raise AppValidationError([
            f'Описание больше {TestLimits.CONTENT_MAX_LENGTH} символов'
        ])


def validate_test_min_tags(*, test: Test) -> None:
    if not test.tags.exists():
        raise PublishValidationError([
            TestMessages.REQUIRED_TAG,
        ])


def validate_test_questions_count(*, test: Test) -> None:
    questions_count = test.questions.count()

    if questions_count < QuestionLimits.MIN_QUESTIONS_FOR_PUBLISH:
        raise PublishValidationError([
            f'Для публикации необходимо минимум {QuestionLimits.MIN_QUESTIONS_FOR_PUBLISH} вопроса '
        ])


def validate_test_questions(*, test: Test) -> None:
    errors = []

    questions = test.questions.all()

    for number, question in enumerate(questions, start=1):
        validate_question_text(
            text=question.text,
            max_length=QuestionLimits.TITLE_MAX_LENGTH,
        )

        validate_question_type(
            question_type=question.type,
        )

        try:
            validate_question_for_publish(
                question=question,
                number=number,
            )

        except PublishValidationError as exc:
            errors.extend(exc.details['errors'])

    if errors:
        raise PublishValidationError(errors)
