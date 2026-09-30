from django.db import transaction
from django.http import HttpRequest
from django.template.loader import render_to_string

from ..constants.limits import AnswerLimits
from ..models.answer import Answer
from ..models.question import Question
from ..permissions import check_test_author, check_test_not_published
from ..validators.answer import validate_answer_text, validate_answer_limit, validate_answer_exists

from apps.users.models import User


@transaction.atomic
def create_answer(
    *,
    question: Question,
    user: User,
    text: str,
    flag: bool,
) -> Answer:
    question.refresh_from_db(
        from_queryset=Question.objects.select_for_update(),
    )

    check_test_author(test=question.test, user=user)
    check_test_not_published(test=question.test)

    validate_answer_limit(question=question)
    validate_answer_text(
        text=text,
        max_length=AnswerLimits.MAX_TITLE_LENGTH,
    )
    validate_answer_exists(
        text=text,
        question=question,
    )

    answer = Answer(
        question=question,
        text=text,
        flag=flag,
    )

    answer.save()

    return answer


@transaction.atomic
def delete_answer(
    *,
    answer: Answer,
    user: User,
) -> None:
    question = answer.question

    question.refresh_from_db(
        from_queryset=Question.objects.select_for_update(),
    )

    check_test_author(
        test=question.test,
        user=user,
    )
    check_test_not_published(
        test=question.test,
    )

    answer.delete()


def update_answer_text(
    *,
    answer: Answer,
    user: User,
    text: str,
) -> Answer:
    question = answer.question

    check_test_author(test=question.test, user=user)
    check_test_not_published(test=question.test)

    validate_answer_text(
        text=text,
        max_length=AnswerLimits.MAX_TITLE_LENGTH,
    )
    validate_answer_exists(
        text=text,
        question=question,
    )

    answer.text = text
    answer.save(update_fields=['text'])

    return answer


def update_answer_flag(
    *,
    answer: Answer,
    user: User,
    flag: bool,
) -> Answer:
    question = answer.question

    check_test_author(test=question.test, user=user)
    check_test_not_published(test=question.test)

    answer.flag = flag
    answer.save(update_fields=['flag'])

    return answer


def render_answer(
    answer: Answer,
    request: HttpRequest,
) -> str:
    return render_to_string(
        'tests/answer_block.html',
        {
            'answer': answer,
            'counter': answer.question.answers.count()
        },
        request=request,
    )
