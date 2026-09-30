from ..constants.limits import TestLimits
from ..constants.messages import TagMessages
from ..exceptions import BadRequestError
from ..models.test import Test


def validate_tag_limit(*, test: Test) -> None:
    if test.tags.count() >= TestLimits.MAX_TEST_TAGS:
        raise BadRequestError(TagMessages.TAG_LIMIT)


def validate_tag_exists(
    *,
    test: Test,
    tag_id: int
) -> None:
    if test.tags.filter(id=tag_id).exists():
        raise BadRequestError(TagMessages.ALREADY_ADDED)


def validate_tag_not_exists(
    *,
    test: Test,
    tag_id: int,
) -> None:
    if not test.tags.filter(id=tag_id).exists():
        raise BadRequestError(TagMessages.NOT_FOUND)
