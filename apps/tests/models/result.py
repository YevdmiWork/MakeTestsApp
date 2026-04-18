import uuid

from django.db import models
from django.contrib.auth import get_user_model


class TestResult(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    test = models.ForeignKey(
        'Test',
        on_delete=models.CASCADE,
        related_name='results',
    )

    time_create = models.DateTimeField(
        auto_now_add=True
    )

    correct_answers = models.PositiveIntegerField(
        verbose_name='Правильные ответы'
    )

    total_questions = models.PositiveIntegerField(
        verbose_name='Всего вопросов'
    )

    uuid_slug = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Результат теста'
        indexes = [
            models.Index(fields=['test']),
            models.Index(fields=['user']),
        ]
