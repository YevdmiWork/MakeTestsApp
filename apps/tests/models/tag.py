from django.contrib.postgres.indexes import GinIndex
from django.db import models

from ..querysets.tag import TagQuerySet

from ..constants import limits as const


class Tag(models.Model):
    name = models.CharField(
        max_length=const.TagLimits.MAX_TITLE,
        unique=True,
        verbose_name='Тег',
    )

    objects = TagQuerySet.as_manager()

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
