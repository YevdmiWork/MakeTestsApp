from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView

from ..constants.limits import TestLimits
from ..constants.search import SEARCH_PARAM
from ..exceptions import AppValidationError, AppError
from ..forms import AddTestForm, QuestionCreateForm, AnswerCreateForm, TestTitleForm, TestContentForm
from ..mixins import PublishedTestMixin
from ..models.question import Question
from ..models.tag import Tag
from ..models.test import Test
from ..query_selectors import test as test_selector
from ..services import test as test_services


class AllTests(ListView):
    template_name = 'tests/tests_all.html'
    context_object_name = 'tests'
    sort_param = 'sort_by'
    default_sort = 'popular'
    sort_map = {
        'newest': '-time_update',
        'oldest': 'time_update',
        'popular': '-completion',
    }

    def get_tests_queryset(self):
        return test_selector.get_published()

    def get_current_sort(self):
        sort = self.request.GET.get(self.sort_param)
        return self.sort_map.get(sort, self.sort_map[self.default_sort])

    def apply_sort(self, qs):
        sort = self.get_current_sort()
        return qs.order_by(sort)

    def apply_search(self, qs):
        query = (self.request.GET.get(SEARCH_PARAM) or '').strip()
        if query:
            qs = qs.search(query)
        return qs

    def get_queryset(self):
        qs = self.get_tests_queryset()
        qs = self.apply_search(qs)
        qs = self.apply_sort(qs)
        return qs


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
            'title_form': TestTitleForm(instance=self.object),
            'content_form': TestContentForm(instance=self.object),
            'add_question_form': QuestionCreateForm(),
            'add_answer_form': AnswerCreateForm(),
            'available_tags': Tag.objects.exclude_for_test(self.object),
            'MAX_TEST_TAGS': TestLimits.MAX_TEST_TAGS,
            'type_choices': Question.QuestionType.choices,
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
