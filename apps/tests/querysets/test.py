from django.db import models


class TestQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status='published')
