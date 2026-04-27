from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView

from ..exceptions import AppValidationError, AppError
from ..forms import AddTestForm
from ..models.test import Test
from ..selectors.test import all_tests as get_all_tests
from ..services.test import create_test


class AllTests(ListView):
    template_name = 'tests/tests_all.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return get_all_tests()


class AddTest(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'tests/test_add.html'
    form_class = AddTestForm

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = create_test(
                    user=self.request.user,
                    title=form.cleaned_data['title']
                )

        except AppValidationError as e:
            for err in e.errors:
                form.add_error(None, err)
            return self.form_invalid(form)

        except AppError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

        return redirect(self.get_success_url())
