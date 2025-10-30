import uuid
from .models import Test


def generate_unique_slug() -> str:
    return uuid.uuid4().hex[:32]

def create_test(user, cleaned_data):
    title = (cleaned_data.get('title') or '').strip()
    test = Test(
        author=user,
        title=title,
        slug=generate_unique_slug(),
    )
    test.full_clean()
    test.save()
    return test
