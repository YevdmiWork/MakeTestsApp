from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddTestForm
from .models import Test
from .services import create_test


class AllTests(ListView):
    template_name = "tests/tests_all.html"
    context_object_name = "tests"

    def get_queryset(self):
        return Test.published.all()


class BaseTestView(DetailView):
    slug_url_kwarg = 'test_slug'
    context_object_name = 'tests'


class TestView(BaseTestView):
    template_name = 'tests/test_view.html'

    def get_queryset(self):
        return Test.objects.with_test_content().with_test_data()


class TestRun(BaseTestView):
    template_name = 'tests/test_run.html'

    def get_queryset(self):
        return Test.objects.with_fields()


class TestEdit(BaseTestView):
    context_object_name = 'test'
    template_name = 'tests/test_edit.html'

    def get_queryset(self):
        return Test.objects.with_test_status().with_test_content()


class AddTest(LoginRequiredMixin, CreateView):
    model = Test
    template_name = 'tests/add_test.html'
    form_class = AddTestForm

    def form_valid(self, form):
        test = create_test(self.request.user, form.cleaned_data)
        return redirect(test.get_edit_url())

