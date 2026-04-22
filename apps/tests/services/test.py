import uuid
from django.db import transaction

from ..models import Test
from ..validators.test import validate_test_limit, validate_test
from ..constants import limits as const

from apps.users.models import User


class SlugService:
    @staticmethod
    @transaction.atomic
    def generate_slug() -> str:
        while True:
            slug = uuid.uuid4().hex[:const.Test.SLUG_MAX_LENGTH]
            if not Test.objects.filter(slug=slug).exists():
                return slug


def create_test(*, user: User, title: str) -> Test:
    title = (title or '').strip()

    validate_test_limit(user)

    test = Test(
        author=user,
        title=title,
        slug=SlugService.generate_slug(),
    )

    validate_test(test)

    test.save()
    return test
