from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .choices import TestStatus
from .tag import Tag
from ..constants import limits as const
from ..querysets.test import TestQuerySet


class Test(models.Model):
    title = models.CharField(
        max_length=const.TestLimits.TITLE_MAX_LENGTH,
        verbose_name='Название теста',
        blank=False,
        null=False,
    )

    content = models.CharField(
        max_length=const.TestLimits.CONTENT_MAX_LENGTH,
        verbose_name='Описание',
        blank=True,
        null=False,
        default='Нет описания',
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен',
    )

    slug = models.CharField(
        max_length=const.TestLimits.SLUG_MAX_LENGTH,
        verbose_name='Альт.название',
        blank=False,
        null=False,
        unique=True,
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='tests',
        null=False,
        blank=False,
    )

    rating_avg = models.FloatField(
        verbose_name='Оценка',
        default=0,
        blank=False,
        null=False,
    )

    rating_count = models.IntegerField(
        verbose_name='кол-во оценок',
        default=0,
        blank=False,
        null=False,
    )

    completion = models.IntegerField(
        verbose_name='Количество прохождений',
        default=0,
        blank=False,
        null=False,
    )

    status = models.CharField(
        max_length=const.TestLimits.STATUS_MAX_LENGTH,
        choices=TestStatus.choices,
        default=TestStatus.UNPUBLISHED,
        verbose_name='Статус',
    )

    tag = models.ManyToManyField(
        Tag,
        related_name='tests',
        blank=True,
        verbose_name='Теги',
    )

    objects = TestQuerySet.as_manager()

    def get_preview_url(self):
        return reverse('pages:preview', kwargs={'test_slug': self.slug})

    def get_edit_url(self):
        return reverse('pages:edit', kwargs={'test_slug': self.slug})

    class Meta:
        ordering = ['-completion']
        indexes = [
            models.Index(fields=['completion']),
            models.Index(fields=['status',
                                 'author']),
            GinIndex(
                fields=['title'],
                name='test_title_trgm',
                opclasses=['gin_trgm_ops'],
            ),
            GinIndex(
                fields=['content'],
                name='test_content_trgm',
                opclasses=['gin_trgm_ops'],
            ),
        ]

