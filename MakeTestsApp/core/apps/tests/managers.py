from django.db import models

from .querysets import TestQuerySet, QuestionQuerySet


class PublishedTestManager(models.Manager):
    def get_queryset(self):
        return (
            TestQuerySet(self.model, using=self._db)
            .published()
        )


class QuestionManager(models.Manager):
    def get_queryset(self):
        return (
            QuestionQuerySet(self.model, using=self._db)
        )

    def with_answers(self):
        return self.get_queryset().with_answers()

    def for_test(self, test):
        return self.get_queryset().for_test(test)
