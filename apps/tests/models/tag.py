from django.contrib.postgres.indexes import GinIndex
from django.db import models

from ..constants import limits as const


class Tag(models.Model):
    name = models.CharField(
        max_length=const.Tag.MAX_TITLE,
        unique=True,
        verbose_name='Тег',
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            GinIndex(
                fields=['name'],
                name='tag_name_trgm',
                opclasses=['gin_trgm_ops'],
            )
        ]
