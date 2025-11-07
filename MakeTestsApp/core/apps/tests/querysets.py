from django.db.models import Count, Q, Prefetch
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
        queryset = self.select_related('author').prefetch_related('tag').only(*fields)
        queryset._extra_fields = fields
        return queryset

    def published(self):
        return self.filter(status='published')

    def with_test_data(self):
        return self.with_fields([
            'rating',
            'completion',
        ])

    def with_test_content(self):
        return self.with_fields([
            'content',
        ])

    def with_test_status(self):
        return self.with_fields([
            'status',
        ])

    def by_author_username(self, username: str):
        return self.filter(author__username=username).order_by('-time_create')

    def similar_to(self, test, limit=4):
        test_tags = test.tag.values_list('id', flat=True)
        return (
            self.exclude(id=test.id)
            .filter(tag__in=test_tags)
            .annotate(common_tags=Count('tag', filter=Q(tag__in=test_tags)))
            .order_by('-common_tags', '-completion')
            .select_related('author')
            .only(
                'id',
                'title',
                'slug',
                'completion',
                'rating',
                'author_id',
                'author__username'
            )
            .prefetch_related('tag')
            .distinct()[:limit]
        )


class QuestionQuerySet(models.QuerySet):
    def with_answers(self):
        return self.prefetch_related('answers').only(
            'text',
            'image',
            'type',
        )

    def for_test(self, test):
        from .models import Answer
        return (
            self.filter(test=test)
            .only('id', 'text', 'image', 'type')
            .prefetch_related(
                Prefetch(
                    'answers',
                    queryset=Answer.objects.only(
                        'id', 'question_id', 'text',
                    ).order_by('id'),
                    to_attr='prefetched_answers',
                )
            )
        )
