from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import RegisterUserForm, LoginUserForm, UserPasswordChangeForm
from .mixins import ProfileTestsMixin
from .services import register_user

from apps.tests.selectors.test import for_profile as tests_for_profile


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = register_user(self.request, form)
        return redirect('pages:home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('pages:home')


class LogoutUser(LogoutView):
    next_page = 'users:login'


class ProfileUser(ProfileTestsMixin, ListView):
    template_name = "users/profile.html"
    context_object_name = 'tests'

    def get_queryset(self):
        return tests_for_profile(
            user=self.profile_user,
            viewer=self.request.user
        )


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
