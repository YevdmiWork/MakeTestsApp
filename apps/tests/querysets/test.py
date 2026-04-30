from django.db import models
from django.db.models import Count, Q

from ..models.choices import TestStatus


class TestQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status=TestStatus.PUBLISHED)

    def by_author(self, user):
        return self.filter(author=user)

    def similar_to(self, test):
        return (
            self.exclude(id=test.id)
            .annotate(
                common_tags=Count(
                    'tag',
                    filter=Q(tag__in=test.tag.all()),
                    distinct=True
                )
            )
            .filter(common_tags__gt=0)
            .order_by(
                '-common_tags',
                '-completion',
            )
        )
