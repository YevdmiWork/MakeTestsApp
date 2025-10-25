from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from .services import register_user, get_user_tests


class ProfileUser(ListView):
    template_name = "users/profile.html"
    context_object_name = 'tests'

    def get_queryset(self):
        return get_user_tests(self.kwargs.get('username'))


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        register_user(self.request, form)
        return redirect('tests:home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('tests:home')


def logout_user(request):
    logout(request)
    return redirect('users:login')


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
