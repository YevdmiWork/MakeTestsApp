from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from django.db.models import Count, Q, OuterRef, FloatField, Subquery, F
from django.db.models.functions import Coalesce

from ..constants.search import SEARCH_WEIGHTS, SEARCH_THRESHOLD, SEARCH_ORDERING
from ..models.choices import TestStatus
from ..models.tag import Tag


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
                    'tags',
                    filter=Q(tags__in=test.tags.all()),
                    distinct=True
                )
            )
            .filter(common_tags__gt=0)
            .order_by(
                '-common_tags',
                '-completion',
            )
        )

    def search(self, query):
        tag_sim_subquery = (
            Tag.objects
            .filter(tests=OuterRef('pk'))
            .annotate(similar=TrigramSimilarity('name', query))
            .order_by('-similar')
            .values('similar')[:1]
        )

        return (
            self.annotate(
                title_similarity=TrigramSimilarity(
                    'title',
                    query
                ),
                content_similarity=TrigramSimilarity(
                    'content',
                    query
                ),
                author_similarity=TrigramSimilarity(
                    'author__username',
                    query
                ),
                tag_similarity=Coalesce(
                    Subquery(
                        tag_sim_subquery,
                        output_field=FloatField()),
                    0.0
                ),
            )
            .annotate(
                similarity=(
                    F('title_similarity') * SEARCH_WEIGHTS['title'] +
                    F('content_similarity') * SEARCH_WEIGHTS['content'] +
                    F('tag_similarity') * SEARCH_WEIGHTS['tag'] +
                    F('author_similarity') * SEARCH_WEIGHTS['author']
                )
            )
            .filter(similarity__gt=SEARCH_THRESHOLD)
            .order_by(*SEARCH_ORDERING)
        )
