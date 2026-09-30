from django.shortcuts import get_object_or_404

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
