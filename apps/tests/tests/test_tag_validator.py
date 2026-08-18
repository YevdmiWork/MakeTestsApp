import pytest

from ..constants.limits import TestLimits
from ..exceptions import BadRequestError
from ..validators.tag import (
    validate_tag_limit,
    validate_tag_exists,
    validate_tag_not_exists,
)

class TestValidateTagLimit:
    def test_less_than_limit(self, test, tag_factory):
        for i in range(TestLimits.MAX_TEST_TAGS - 1):
            test.tag.add(tag_factory(name=f'tag-{i}'))

        validate_tag_limit(test=test)

    def test_equal_limit(self, test, tag_factory):
        for i in range(TestLimits.MAX_TEST_TAGS):
            test.tag.add(tag_factory(name=f'tag-{i}'))

        with pytest.raises(BadRequestError):
            validate_tag_limit(test=test)


class TestValidateTagExists:
    def test_tag_not_added(self, test, tag):
        validate_tag_exists(
            test=test,
            tag_id=tag.id,
        )

    def test_tag_already_added(self, test, tag):
        test.tag.add(tag)

        with pytest.raises(BadRequestError):
            validate_tag_exists(
                test=test,
                tag_id=tag.id,
            )


class TestValidateTagNotExists:
    def test_tag_not_added(self, test, tag):
        with pytest.raises(BadRequestError):
            validate_tag_not_exists(
                test=test,
                tag_id=tag.id,
            )

    def test_tag_added(self, test, tag):
        test.tag.add(tag)

        validate_tag_not_exists(
            test=test,
            tag_id=tag.id,
        )
