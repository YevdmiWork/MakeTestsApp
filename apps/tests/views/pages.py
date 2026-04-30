from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView

from ..constants.limits import TestLimits
from ..exceptions import AppValidationError, AppError
from ..forms import AddTestForm, QuestionCreateForm, AnswerCreateForm, TestEditForm
from ..mixins import PublishedTestMixin
from ..models.tag import Tag
from ..models.test import Test
from ..selectors import test as test_selector
from ..services import test as test_services


class AllTests(ListView):
    template_name = 'tests/tests_all.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return test_selector.get_published()


class AddTest(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'tests/test_add.html'
    form_class = AddTestForm

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = test_services.create_test(
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


class BaseTestView(DetailView):
    slug_url_kwarg = 'test_slug'
    context_object_name = 'test'


class TestEdit(LoginRequiredMixin, BaseTestView):
    template_name = 'tests/test_edit.html'

    def get_queryset(self):
        return test_selector.get_for_edit(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'test_edit_form': TestEditForm(instance=self.object),
            'add_question_form': QuestionCreateForm(),
            'add_answer_form': AnswerCreateForm(),
            'available_tags': Tag.objects.exclude_for_test(self.object),
            'MAX_TEST_TAGS': TestLimits.MAX_TEST_TAGS,
        })
        return context


class TestPreview(PublishedTestMixin, BaseTestView):
    template_name = 'tests/test_preview.html'

    def get_queryset(self):
        return test_selector.get_preview()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_tests'] = test_selector.get_similar(test=self.object)
        return context
