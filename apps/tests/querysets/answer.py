from django.db import models


class AnswerQuerySet(models.QuerySet):
    def by_author(self, user):
        return self.filter(question__test__author=user)
