from django.views.generic import ListView, DetailView, CreateView
from .models import Test


class AllTests(ListView):
    template_name = "tests/tests_all.html"
    context_object_name = "tests"
    model = Test


class BaseTestView(DetailView):
    slug_url_kwarg = 'test_slug'
    context_object_name = 'tests'


class TestView(BaseTestView):
    template_name = 'tests/test_view.html'


class TestRun(BaseTestView):
    template_name = 'tests/test_run.html'


class TestEdit(BaseTestView):
    context_object_name = 'test'
    template_name = 'tests/test_edit.html'


class AddTest(CreateView):
    model = Test
    template_name = 'tests/add_test.html'
