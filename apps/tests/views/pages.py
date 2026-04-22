from django.views.generic import ListView

from ..selectors.test import TestSelector


class AllTests(ListView):
    template_name = 'tests/tests_all.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return TestSelector.get_all_tests()
