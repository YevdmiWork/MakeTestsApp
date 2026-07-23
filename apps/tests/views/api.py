from .serializers import serialize_tag, serialize_test
from ..decorators import post_api
from ..exceptions import AppValidationError, BadRequest
from ..forms import TestTitleForm, TestContentForm, TagForm
from ..query_selectors.test import get_test_or_404
from ..services import tag as tag_service
from ..services import test as test_service


TEST_INFO_FIELDS = {
    'title': TestTitleForm,
    'content': TestContentForm,
}

def raise_form_error(form):
    raise AppValidationError([
        err
        for field_errors in form.errors.values()
        for err in field_errors
    ])


@post_api
def update_test_info(request, test_id):
    test = get_test_or_404(test_id, request.user)

    for field_name, form_class in TEST_INFO_FIELDS.items():
        if field_name not in request.POST:
            continue

        form = form_class(request.POST)

        if not form.is_valid():
            raise_form_error(form)

        test = test_service.update_test(
            test=test,
            user=request.user,
            **form.cleaned_data,
        )

        return {
            'test': serialize_test(test),
        }

    raise BadRequest('Expected one of: title, content')


@post_api
def add_tag(request, test_id):
    test = get_test_or_404(test_id, request.user)

    form = TagForm(request.POST)
    if not form.is_valid():
        raise_form_error(form)

    tag = tag_service.add_tag_to_test(
        test=test,
        user=request.user,
        tag_id=form.cleaned_data['tag_id'],
    )

    return {
        'tag': serialize_tag(tag),
    }


@post_api
def remove_tag(request, test_id):
    test = get_test_or_404(test_id, request.user)

    form = TagForm(request.POST)
    if not form.is_valid():
        raise_form_error(form)

    tag = tag_service.remove_tag_from_test(
        test=test,
        user=request.user,
        tag_id=form.cleaned_data['tag_id'],
    )

    return {
        'tag': serialize_tag(tag),
    }
