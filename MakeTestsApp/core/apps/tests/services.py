import uuid
from .models import Test


def generate_unique_slug() -> str:
    return uuid.uuid4().hex[:32]

def create_test(user, cleaned_data):
    test = Test(
        author=user,
        title=cleaned_data['title'],
        slug=generate_unique_slug(),
    )
    test.save()
    return test
