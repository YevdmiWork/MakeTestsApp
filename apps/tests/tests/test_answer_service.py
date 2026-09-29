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


@pytest.mark.django_db
def test_update_answer_text(answer, user):
    new_text = 'update this answer'

    result = answer_service.update_answer_text(
        answer=answer,
        user=user,
        text=new_text,
    )

    assert result is answer

    answer.refresh_from_db()

    assert answer.text == new_text


@pytest.mark.django_db
def test_update_answer_flag(answer, user):
    new_flag = not answer.flag

    result = answer_service.update_answer_flag(
        answer=answer,
        user=user,
        flag=new_flag,
    )

    assert result is answer

    answer.refresh_from_db()

    assert answer.flag is new_flag
