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
