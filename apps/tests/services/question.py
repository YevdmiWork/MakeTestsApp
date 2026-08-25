from django.http import HttpRequest
from django.template.loader import render_to_string

from ..forms import AnswerCreateForm
from ..models.question import Question
from ..models.test import Test
from ..permissions import check_test_author, check_test_not_published

from ..constants import limits as const
from ..validators import question as question_validators

from apps.users.models import User


def create_question(
    *,
    test: Test,
    user: User,
    text: str,
) -> Question:

    check_test_author(test=test, user=user)
    check_test_not_published(test=test)

    question_validators.validate_question_text(
        text=text,
        max_length=const.QuestionLimits.TITLE_MAX_LENGTH,
    )

    question = Question(
        test=test,
        text=text,
    )

    question.save()
    return question


def delete_question(
    *,
    question: Question,
    user: User,
) -> None:

    check_test_author(test=question.test, user=user)
    check_test_not_published(test=question.test)

    question.delete()


def update_question_text(
    *,
    question: Question,
    user: User,
    text: str,
) -> Question:

    check_test_author(test=question.test, user=user)
    check_test_not_published(test=question.test)

    question_validators.validate_question_text(
        text=text,
        max_length=const.QuestionLimits.TITLE_MAX_LENGTH,
    )

    question.text = text
    question.save(update_fields=['text'])

    return question


def update_question_type(
    *,
    question: Question,
    user: User,
    question_type: str,
) -> Question:

    check_test_author(test=question.test, user=user)
    check_test_not_published(test=question.test)

    question_validators.validate_question_type(
        question_type=question_type,
    )

    question.type = question_type
    question.save(update_fields=['type'])

    return question


def render_question(
    question: Question,
    test: Test,
    request: HttpRequest,
) -> str:
    return render_to_string(
        'tests/question_block.html',
        {
            'question': question,
            'question_number': test.questions.count(),
            'add_answer_form': AnswerCreateForm(),
            'type_choices': Question.QuestionType.choices,
        },
        request=request,
    )
