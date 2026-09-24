import pytest

from ..services import answer as answer_service


@pytest.mark.django_db
def test_create_answer(question, user):
    text = 'true answer'

    result = answer_service.create_answer(
        question=question,
        user=user,
        text=text,
        flag=True,
    )

    assert result.text == text
    assert result.question is question
    assert result.flag is True
    assert result.pk is not None
