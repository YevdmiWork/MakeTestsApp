from django.core.exceptions import ValidationError

from ..constants.limits import TestLimits
from ..exceptions import AppValidationError
from ..models.test import Test
from ..constants import limits as const

from apps.users.models import User


def validate_test_limit(user: User) -> None:
    if Test.objects.filter(author=user).count() >= const.TestLimits.MAX_TESTS_FOR_USER:
        raise AppValidationError(['Лимит тестов'])


def validate_test(test: Test) -> None:
    try:
        test.full_clean()
    except ValidationError as e:
        raise AppValidationError(e.messages)


def validate_test_title(title: str | None):
    if not title:
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


def validate_test_content(content: str | None):
    if not content:
        return

    content = content.strip()
    content_length = len(content)

    if content_length > TestLimits.CONTENT_MAX_LENGTH:
        raise AppValidationError([
            f'Описание больше {TestLimits.CONTENT_MAX_LENGTH} символов'
        ])
