from django.db import models

from ..querysets.question import QuestionQuerySet

from ..constants import limits as const


class Question(models.Model):

    class QuestionType(models.TextChoices):
        SINGLE_CHOICE = 'SC', 'Один вариант'
        MULTIPLE_CHOICES = 'MC', 'Несколько вариантов'
        TEXT_FIELD = 'TF', 'Текстовое поле'

    test = models.ForeignKey(
        'Test',
        on_delete=models.CASCADE,
        verbose_name='Связанный тест',
        related_name='questions',
    )

    text = models.CharField(
        max_length=const.QuestionLimits.TITLE_MAX_LENGTH,
        verbose_name='Вопрос',
        blank=False,
        null=False,
    )

    image = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
    )

    type = models.CharField(
        max_length=2,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE_CHOICE,
        verbose_name='Тип вопроса',
    )

    objects = QuestionQuerySet.as_manager()

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['type']),
        ]
