from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from ..constants.limits import TestLimits
from ..models.question import Question
from ..models.test import Test


def get_published():
    qs = (
        Test.objects
        .published()
        .select_related('author')
        .prefetch_related('tag')
        .only(
            'id',
            'title',
            'time_update',
            'slug',
            'author_id',
            'rating_avg',
            'completion',
            'author__username',
        )
    )
    return qs


def get_for_profile(user, viewer):
    qs = (
        Test
        .objects
        .by_author(user)
    )

    if not viewer.is_authenticated or viewer != user:
        qs = qs.published()

    qs = qs.only(
        'id',
        'slug',
        'time_create',
        'title',
        'rating_avg',
        'completion',
        'status',
        'author_id',
    )
    return qs


def get_for_edit(user):
    qs = (
        Test.objects
        .by_author(user)
        .select_related('author')
        .prefetch_related(
            'tag',
            Prefetch(
                'questions',
                queryset=Question.objects.prefetch_related('answers'),
            )
        )
        .only(
            'id',
            'title',
            'time_update',
            'slug',
            'author_id',
            'rating_avg',
            'completion',
            'content',
            'status',
            'author__username',
        )
    )
    return qs


def get_preview():
    qs = (
        Test.objects
        .published()
        .select_related('author')
        .prefetch_related('tag')
        .only(
            'id',
            'title',
            'slug',
            'completion',
            'rating_avg',
            'time_update',
            'rating_count',
            'status',
            'content',
            'author_id',
            'author__username'
        )
    )
    return qs


def get_similar(test, limit=TestLimits.SIMILAR_TESTS_LIMIT):
    qs = (
        Test.objects
        .published()
        .similar_to(test)
        .select_related('author')
        .prefetch_related('tag')
        .only(
            'id',
            'title',
            'slug',
            'completion',
            'rating_avg',
            'time_update',
            'rating_count',
            'status',
            'content',
            'author_id',
            'author__username'
        )[:limit]
    )
    return qs


def get_test_or_404(test_id, user):
    return get_object_or_404(
        Test.objects.by_author(user),
        id=test_id
    )
