import pytest
from django.contrib.auth import get_user_model

from ..models.question import Question
from ..models.tag import Tag
from ..models.test import Test


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


@pytest.fixture
def tag(db):
    return Tag.objects.create(
        name='IQ',
    )


@pytest.fixture
def tag_factory(db):
    def factory(name):
        return Tag.objects.create(name=name)
    return factory


@pytest.fixture
def question(test):
    return Question.objects.create(
        test=test,
        text='How much is 2-2= ?',
    )
