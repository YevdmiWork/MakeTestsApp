import pytest
from django.contrib.auth import get_user_model

from apps.tests.models.test import Test


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username='username',
        password='userpassword'
    )


@pytest.fixture
def test(user):
    return Test.objects.create(
        title='Test title',
        content='Test content',
        slug='test-slug',
        author=user,
    )
