from .constants.messages import TestMessages
from .exceptions import AccessDeniedError, ConflictError
from .models.choices import TestStatus


def check_test_author(*, test, user):
    if test.author_id != user.id:
        raise AccessDeniedError(TestMessages.NOT_AUTHOR)


def check_test_not_published(*, test):
    if test.status == TestStatus.PUBLISHED:
        raise ConflictError(TestMessages.ALREADY_PUBLISHED)
