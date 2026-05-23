from ..decorators import post_api
from ..exceptions import AppValidationError, BadRequest
from ..forms import TestTitleForm, TestContentForm
from ..query_selectors.test import get_test_or_404
from ..services.test import update_test


TEST_INFO_FIELDS = {
    'title': TestTitleForm,
    'content': TestContentForm,
}


@post_api
def update_test_info(request, test_id):
    test = get_test_or_404(test_id, request.user)

    for field_name, form_class in TEST_INFO_FIELDS.items():
        if field_name not in request.POST:
            continue

        form = form_class(request.POST)

        if not form.is_valid():
            errors = [
                e["message"]
                for field_errors in form.errors.get_json_data().values()
                for e in field_errors
            ]

            raise AppValidationError(errors)

        return update_test(
            test=test,
            user=request.user,
            **form.cleaned_data
        )

    raise BadRequest('Expected one of: title, content')
