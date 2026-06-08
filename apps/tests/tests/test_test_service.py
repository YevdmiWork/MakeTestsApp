import pytest

from ..exceptions import AppValidationError
from ..services.test import update_test


@pytest.mark.django_db
def test_update_content(test, user):
    new_content = 'New content'

    result = update_test(
        test=test,
        user=user,
        content=new_content,
    )

    test.refresh_from_db()

    assert test.content == new_content

    assert result == {
        'test': {
            'id': test.id,
            'title': test.title,
            'content': new_content,
        }
    }


@pytest.mark.django_db
def test_update_title(test, user):
    new_title = 'New title'

    result = update_test(
        test=test,
        user=user,
        title=new_title,
    )

    test.refresh_from_db()

    assert test.title == new_title

    assert result == {
        'test': {
            'id': test.id,
            'title': new_title,
            'content': test.content,
        }
    }


@pytest.mark.django_db
def test_none_values(test, user):
    old_title = test.title
    old_content = test.content

    result = update_test(
        test=test,
        title=None,
        content=None,
        user=user,
    )

    test.refresh_from_db()

    assert test.title == old_title
    assert test.content == old_content

    assert result == {
        'test': {
            'id': test.id,
            'title': old_title,
            'content': old_content,
        }
    }


@pytest.mark.django_db
def test_empty_title(test, user):
    with pytest.raises(AppValidationError):
        update_test(
            test=test,
            title='',
            user=user,
        )
