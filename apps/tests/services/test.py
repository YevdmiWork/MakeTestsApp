import uuid
from typing import Any

from django.db import transaction

from ..models.choices import TestStatus
from ..models.question import Question
from ..models.result import TestResult
from ..models.test import Test
from ..permissions import check_test_author, check_test_not_published

from ..validators import test as test_validators
from ..validators import answer as answer_validators
from ..constants import limits as const
from ..query_selectors import question as question_selector

from apps.users.models import User


def generate_slug() -> str:
    return uuid.uuid4().hex[:const.TestLimits.SLUG_MAX_LENGTH]


@transaction.atomic
def create_test(
    *,
    user: User,
    title: str
) -> Test:
    user = User.objects.select_for_update().get(pk=user.pk)

    title = title.strip()

    test_validators.validate_test_limit(user=user)
    test_validators.validate_test_title(title=title)

    test = Test(
        author=user,
        title=title,
        slug=generate_slug(),
    )

    test_validators.validate_test(test=test)

    test.save()
    return test


def update_test(
    *,
    test: Test,
    title: str | None = None,
    content: str | None = None,
    user: User,
) -> Test:

    check_test_author(test=test, user=user)
    check_test_not_published(test=test)

    update_fields = []

    if title is not None:
        title = title.strip()
        test_validators.validate_test_title(title=title)

        test.title = title
        update_fields.append('title')

    if content is not None:
        content = content.strip()
        test_validators.validate_test_content(content=content)

        test.content = content
        update_fields.append('content')

    if update_fields:
        test.save(update_fields=update_fields)

    return test


@transaction.atomic
def publish_test(
    *,
    test: Test,
    user: User,
) -> Test:
    test.refresh_from_db(
        from_queryset=Test.objects.select_for_update(),
    )

    check_test_author(test=test, user=user)
    check_test_not_published(test=test)

    test_validators.validate_test_min_tags(test=test)
    test_validators.validate_test_questions_count(test=test)
    test_validators.validate_test_questions(test=test)

    test.status = TestStatus.PUBLISHED
    test.save(update_fields=['status', 'time_update'])

    return test


def unpublish_test(
    *,
    test: Test,
    user: User,
) -> Test:

    check_test_author(test=test, user=user)

    test.status = TestStatus.UNPUBLISHED
    test.save(update_fields=['status', 'time_update'])

    return test


@transaction.atomic
def complete_test(
    *,
    test: Test,
    user: User | None,
    answers: dict,
) -> TestResult:
    test = Test.objects.select_for_update().get(pk=test.pk)

    questions = list(
        question_selector.get_for_result(test=test)
    )

    answers = answer_validators.validate_answers(
        questions=questions,
        answers=answers,
    )

    correct_answers = calculate_result(
        questions=questions,
        answers=answers,
    )

    result = save_result(
        test=test,
        user=user,
        correct_answers=correct_answers,
        total_questions=len(questions),
    )

    increment_completion(test=test)

    return result


def calculate_result(
    *,
    questions: list[Question],
    answers: dict[str, Any],
) -> int:
    return sum(
        is_correct_answer(
            question=question,
            selected=answers[str(question.id)],
        )
        for question in questions
    )


def is_correct_answer(
    *,
    question: Question,
    selected: Any,
) -> bool:
    correct_answers = list(question.answers.all())

    if question.type == Question.QuestionType.SINGLE_CHOICE:
        return any(
            answer.id == selected and answer.flag
            for answer in correct_answers
        )

    if question.type == Question.QuestionType.MULTIPLE_CHOICES:
        correct_ids = {
            answer.id
            for answer in correct_answers
            if answer.flag
        }
        return set(selected) == correct_ids

    if question.type == Question.QuestionType.TEXT_FIELD:
        correct_texts = {
            answer.text.strip().casefold()
            for answer in correct_answers
            if answer.flag is not None
        }
        return selected.strip().casefold() in correct_texts

    return False


def save_result(
    *,
    test: Test,
    user: User | None,
    correct_answers: int,
    total_questions: int,
) -> TestResult:
    return TestResult.objects.create(
        test=test,
        user=user if user and user.is_authenticated else None,
        correct_answers=correct_answers,
        total_questions=total_questions,
    )


def increment_completion(*, test: Test) -> Test:
    test.completion += 1
    test.save(
        update_fields=[
            'completion',
            'time_update',
        ],
    )
    return test
