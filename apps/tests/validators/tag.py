from ..constants.limits import TestLimits
from ..exceptions import BadRequest
from ..models.test import Test


def validate_tag_limit(*, test: Test) -> None:
    if test.tag.count() >= TestLimits.MAX_TEST_TAGS:
        raise BadRequest('Лимит тегов')


def validate_tag_exists(
    *,
    test: Test,
    tag_id: int
) -> None:
    if test.tag.filter(id=tag_id).exists():
        raise BadRequest('Тег уже добавлен')


def validate_tag_not_exists(
    *,
    test: Test,
    tag_id: int,
) -> None:
    if not test.tag.filter(id=tag_id).exists():
        raise BadRequest('Тег не найден')
