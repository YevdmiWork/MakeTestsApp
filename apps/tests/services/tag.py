from django.db import transaction

from ..models.tag import Tag
from ..models.test import Test
from ..permissions import check_test_author, check_test_not_published
from ..query_selectors.tag import tag_get_by_id

from ..validators import tag as test_validators

from apps.users.models import User


@transaction.atomic
def add_tag_to_test(
    *,
    test: Test,
    user: User,
    tag_id: int,
) -> Tag:

    check_test_author(test=test, user=user)
    check_test_not_published(test=test)

    test_validators.validate_tag_limit(test=test)
    test_validators.validate_tag_exists(
        test=test,
        tag_id=tag_id
    )

    tag = tag_get_by_id(tag_id=tag_id)

    test.tags.add(tag)

    return tag


def remove_tag_from_test(
    *,
    test: Test,
    user: User,
    tag_id: int,
) -> Tag:

    check_test_author(test=test, user=user)
    check_test_not_published(test=test)

    test_validators.validate_tag_not_exists(
        test=test,
        tag_id=tag_id,
    )

    tag = tag_get_by_id(tag_id=tag_id)

    test.tags.remove(tag)

    return tag

