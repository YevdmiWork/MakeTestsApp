import pytest

from ..services import question as question_service

@pytest.mark.django_db
def test_create_question(test, user):
    text = '2 + 2 ='

    result = question_service.create_question(
        test=test,
        user=user,
        text=text,
    )

    assert result.text == text
    assert result.test is test
    assert result.pk is not None
