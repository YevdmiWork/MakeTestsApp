from django.db import models


class TagQuerySet(models.QuerySet):

    def exclude_for_test(self, test):
        return self.exclude(tests=test)
