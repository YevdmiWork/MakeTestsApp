from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .managers import TestQuerySet, PublishedTestManager


class TestStatus(Enum):
    PUBLISHED = 'published'
    UNPUBLISHED = 'unpublished'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class Tag(models.Model):
    name = models.CharField(
        max_length=24,
        unique=True,
        verbose_name='Тег')

    def __str__(self):
        return self.name


class Test(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название теста',
        blank=False,
        null=False,
    )

    content = models.CharField(
        max_length=1500,
        verbose_name='Описание',
        blank=True,
        null=False,
        default='Нет описания',
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )

    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен'
    )

    slug = models.CharField(
        verbose_name='Альт.название',
        max_length=32,
        blank=False,
        null=False,
        unique=True,
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='author_tests',
        null=False,
        blank=False,
        default=None,
    )

    rating = models.IntegerField(
        verbose_name='Оценка',
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
        max_length=30,
        choices=TestStatus.choices(),
        default=TestStatus.UNPUBLISHED.value,
        verbose_name='Статус'
    )

    tag = models.ManyToManyField(
        Tag,
        related_name='tests',
        blank=True,
        verbose_name='Теги'
    )

    objects = TestQuerySet.as_manager()
    published = PublishedTestManager()

    class Meta:
        ordering = ['-completion']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tests:test_view', kwargs={'test_slug': self.slug})

    def get_edit_url(self):
        return reverse('tests:test_edit', kwargs={'test_slug': self.slug})

    def get_run_url(self):
        return reverse('tests:test_run', kwargs={'test_slug': self.slug})

