from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from .test import Test

from ..constants import limits as const


class Rating(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='test_rating'
    )

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='rating'
    )

    value = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(const.RatingLimits.MIN_VALUE),
            MaxValueValidator(const.RatingLimits.MAX_VALUE),
        ]
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    class Meta:
        unique_together = (
            'user',
            'test',
        )
