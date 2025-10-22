from django.db import models
from django.contrib.auth import get_user_model

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

    class Meta:
        ordering = ["-completion"]

    def __str__(self):
        return self.title
