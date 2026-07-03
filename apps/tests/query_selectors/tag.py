from ..models.tag import Tag


def tag_get_by_id(*, tag_id: int) -> Tag:
    tag = (
        Tag.objects
        .get(id=tag_id)
    )
    return tag
