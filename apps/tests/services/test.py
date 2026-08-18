import uuid
from django.db import transaction

from ..models.test import Test
from ..permissions import check_test_author, check_test_not_published

from ..validators import test as test_validators
from ..constants import limits as const

from apps.users.models import User


class SlugService:
    @staticmethod
    @transaction.atomic
    def generate_slug() -> str:
        while True:
            slug = uuid.uuid4().hex[:const.TestLimits.SLUG_MAX_LENGTH]
            if not Test.objects.filter(slug=slug).exists():
                return slug


def create_test(
    *,
    user: User,
    title: str
) -> Test:
    title = (title or '').strip()

    test_validators.validate_test_limit(user=user)
    test_validators.validate_test_title(title=title)

    test = Test(
        author=user,
        title=title,
        slug=SlugService.generate_slug(),
    )

    test_validators.validate_test(test=test)

    test.save()
    return test


@transaction.atomic
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
