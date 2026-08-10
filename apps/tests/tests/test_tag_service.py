import pytest

from ..services import tag as tag_service


@pytest.mark.django_db
def test_add_tag_to_test(test, user, tag):
    result = tag_service.add_tag_to_test(
        test=test,
        user=user,
        tag_id=tag.id,
    )

    assert result == tag

    assert test.tag.filter(id=tag.id).exists()


@pytest.mark.django_db
def test_remove_tag_from_test(test, user, tag):
    test.tag.add(tag)

    result = tag_service.remove_tag_from_test(
        test=test,
        user=user,
        tag_id=tag.id,
    )

    assert result == tag

    assert not test.tag.filter(id=tag.id).exists()
