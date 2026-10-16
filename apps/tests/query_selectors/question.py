from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from ..models.answer import Answer
from ..models.question import Question

from apps.users.models import User


def get_question_or_404(
    *,
    question_id: int,
    user: User,
) -> Question:
    return get_object_or_404(
        Question.objects.by_author(user),
        id=question_id
    )


def get_for_result(*, test):
    qs = (
        Question.objects
        .filter(test=test)
        .prefetch_related(
            Prefetch(
                'answers',
                queryset=Answer.objects.only(
                    'id',
                    'question_id',
                    'text',
                    'flag',
                ).order_by('id'),
            )
        )
        .only(
            'id',
            'test_id',
            'type',
            'text',
            'image',
        )
        .order_by('id')
    )
    return qs
