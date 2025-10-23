from django.db import models


class TestQuerySet(models.QuerySet):
    base_fields = [
        'id',
        'slug',
        'title',
        'author_id',
        'author__username',
        'time_update',
    ]

    def with_fields(self, extra_fields=None):
        current_fields = getattr(self, '_extra_fields', [])
        fields = list(set(current_fields + self.base_fields + (extra_fields or [])))
        queryset = self.select_related('author').only(*fields)
        queryset._extra_fields = fields
        return queryset

    def published(self):
        return self.filter(status='published')

    def with_test_data(self):
        return self.with_fields([
            'test_rating',
            'test_completion',
        ])

    def with_test_content(self):
        return self.with_fields([
            'test_content',
        ])

    def with_test_status(self):
        return self.with_fields([
            'test_status',
        ])


class PublishedTestManager(models.Manager):
    def get_queryset(self):
        return (
            TestQuerySet(self.model, using=self._db)
            .with_test_data()
            .published()
        )
