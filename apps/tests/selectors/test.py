from ..models.test import Test


def all_tests():
    return (
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


def for_profile(user, viewer):
    qs = (
        Test
        .objects
        .by_author(user)
    )

    if not viewer.is_authenticated or viewer != user:
        qs = qs.published()

    return qs.only(
        'id',
        'slug',
        'time_create',
        'title',
        'rating_avg',
        'completion',
        'status',
        'author_id',
    )
