from django.shortcuts import get_object_or_404

from ..models.answer import Answer

from apps.users.models import User


def get_answer_or_404(
    *,
    answer_id: int,
    user: User,
) -> Answer:
    return get_object_or_404(
        Answer.objects.by_author(user),
        id=answer_id,
    )
