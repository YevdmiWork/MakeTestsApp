from ..models.test import Test


class TestSelector:

    @staticmethod
    def get_all_tests():
        return (
            Test.objects
            .published()
            .select_related('author')
            .values(
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
