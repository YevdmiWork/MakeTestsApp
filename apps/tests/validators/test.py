from django.core.exceptions import ValidationError

from ..exceptions import AppValidationError
from ..models import Test
from ..constants import limits as const


def validate_test_limit(user):
    if Test.objects.filter(author=user).count() >= const.TestLimits.MAX_TESTS_FOR_USER:
        raise AppValidationError(['Лимит тестов'])


def validate_test(test):
    try:
        test.full_clean()
    except ValidationError as e:
        raise AppValidationError(e.messages)
