from ..models.tag import Tag
from ..models.test import Test


def serialize_test(test: Test) -> dict:
    return {
        'id': test.id,
        'title': test.title,
        'content': test.content,
    }


def serialize_tag(tag: Tag) -> dict:
    return {
        'id': tag.id,
        'name': tag.name,
    }
