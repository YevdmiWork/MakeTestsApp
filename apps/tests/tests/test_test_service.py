import pytest

from ..exceptions import AppValidationError
from ..services import test as test_service


@pytest.mark.django_db
def test_update_content(test, user):
    new_content = 'New content'

    result = test_service.update_test(
        test=test,
        user=user,
        content=new_content,
    )

    assert result is test

    test.refresh_from_db()

    assert test.content == new_content


@pytest.mark.django_db
def test_update_title(test, user):
    new_title = 'New title'

    result = test_service.update_test(
        test=test,
        user=user,
        title=new_title,
    )

    assert result is test

    test.refresh_from_db()

    assert test.title == new_title


@pytest.mark.django_db
def test_none_values(test, user):
    old_title = test.title
    old_content = test.content

    result = test_service.update_test(
        test=test,
        title=None,
        content=None,
        user=user,
    )

    assert result is test

    test.refresh_from_db()

    assert test.title == old_title
    assert test.content == old_content


@pytest.mark.django_db
def test_empty_title(test, user):
    with pytest.raises(AppValidationError):
        test_service.update_test(
            test=test,
            title='',
            user=user,
        )
