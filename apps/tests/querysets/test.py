from django.db import models

from ..models.choices import TestStatus


class TestQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status=TestStatus.PUBLISHED)
