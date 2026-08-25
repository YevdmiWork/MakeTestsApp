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


@pytest.mark.django_db
def test_update_question_text(test, user, question):
    new_text = '2 - 2 ='

    result = question_service.update_question_text(
        question=question,
        user=user,
        text=new_text,
    )

    assert result is question

    question.refresh_from_db()

    assert question.text == new_text
