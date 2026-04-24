from django.db import models

from ..constants import limits as const


class Answer(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        verbose_name='Связанный вопрос',
        related_name='answers',
    )

    text = models.CharField(
        max_length=const.AnswerLimits.MAX_TITLE_LENGTH,
        verbose_name='Ответ',
        blank=False,
        null=False,
    )

    flag = models.BooleanField(
        default=False,
        verbose_name='Правильный ответ',
    )

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['flag']),
        ]
