from .serializers import serialize_tag, serialize_test, serialize_question

from ..decorators import post_api
from ..exceptions import AppValidationError, BadRequestError
from ..forms import TestTitleForm, TestContentForm, TagForm, QuestionForm
from ..query_selectors.question import get_question_or_404
from ..query_selectors.test import get_test_or_404

from ..services import tag as tag_service
from ..services import test as test_service
from ..services import question as question_service


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
    test = get_test_or_404(
        test_id=test_id,
        user=request.user,
    )

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

    raise BadRequestError('Expected one of: title, content')


@post_api
def add_tag(request, test_id):
    test = get_test_or_404(
        test_id=test_id,
        user=request.user,
    )

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
    test = get_test_or_404(
        test_id=test_id,
        user=request.user,
    )

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


@post_api
def add_question(request, test_id):
    test = get_test_or_404(
        test_id=test_id,
        user=request.user,
    )

    form = QuestionForm(request.POST)
    if not form.is_valid():
        raise_form_error(form)

    question = question_service.create_question(
        test=test,
        user=request.user,
        text=form.cleaned_data['text'],
    )

    return {
        'question': serialize_question(question),
        'html': question_service.render_question(
            question,
            request=request,
            test=test,
        ),
    }


@post_api
def delete_question(request, question_id):
    question = get_question_or_404(
        question_id=question_id,
        user=request.user,
    )

    question_service.delete_question(
        question=question,
        user=request.user,
    )

    return {
        'question_id': question_id,
    }


@post_api
def update_question_text(request, question_id):
    question = get_question_or_404(
        question_id=question_id,
        user=request.user,
    )

    form = QuestionForm(request.POST)
    if not form.is_valid():
        raise_form_error(form)

    question = question_service.update_question_text(
        question=question,
        user=request.user,
        text=form.cleaned_data['text'],
    )

    return {
        'question': serialize_question(question),
    }
