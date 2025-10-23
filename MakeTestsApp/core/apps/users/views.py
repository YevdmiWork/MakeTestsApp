from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView


class ProfileUser(ListView):
    template_name = "users/profile.html"
    context_object_name = 'tests'


class RegisterUser(CreateView):
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('tests:home')
