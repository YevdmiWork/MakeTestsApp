import uuid
from django.db import transaction

from ..models.choices import TestStatus
from ..models.test import Test
from ..permissions import check_test_author, check_test_not_published

from ..validators import test as test_validators
from ..constants import limits as const

from apps.users.models import User


def generate_slug() -> str:
    return uuid.uuid4().hex[:const.TestLimits.SLUG_MAX_LENGTH]


@transaction.atomic
def create_test(
    *,
    user: User,
    title: str
) -> Test:
    user = User.objects.select_for_update().get(pk=user.pk)

    title = title.strip()

    test_validators.validate_test_limit(user=user)
    test_validators.validate_test_title(title=title)

    test = Test(
        author=user,
        title=title,
        slug=generate_slug(),
    )

    test_validators.validate_test(test=test)

    test.save()
    return test


def update_test(
    *,
    test: Test,
    title: str | None = None,
    content: str | None = None,
    user: User,
) -> Test:

    check_test_author(test=test, user=user)
    check_test_not_published(test=test)

    update_fields = []

    if title is not None:
        title = title.strip()
        test_validators.validate_test_title(title=title)

        test.title = title
        update_fields.append('title')

    if content is not None:
        content = content.strip()
        test_validators.validate_test_content(content=content)

        test.content = content
        update_fields.append('content')

    if update_fields:
        test.save(update_fields=update_fields)

    return test


@transaction.atomic
def publish_test(
    *,
    test: Test,
    user: User,
) -> Test:
    test.refresh_from_db(
        from_queryset=Test.objects.select_for_update(),
    )

    check_test_author(test=test, user=user)
    check_test_not_published(test=test)

    test_validators.validate_test_min_tags(test=test)
    test_validators.validate_test_questions_count(test=test)
    test_validators.validate_test_questions(test=test)

    test.status = TestStatus.PUBLISHED
    test.save(update_fields=['status', 'time_update'])

    return test


def unpublish_test(
    *,
    test: Test,
    user: User,
) -> Test:

    check_test_author(test=test, user=user)

    test.status = TestStatus.UNPUBLISHED
    test.save(update_fields=['status', 'time_update'])

    return test
