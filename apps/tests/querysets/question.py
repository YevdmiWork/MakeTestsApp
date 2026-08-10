from django.db import models


class QuestionQuerySet(models.QuerySet):
    def by_author(self, user):
        return self.filter(test__author=user)
