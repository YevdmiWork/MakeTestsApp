from django.views.generic import ListView


class AllTests(ListView):

    template_name = 'tests/tests_all.html'
    context_object_name = 'tests'
