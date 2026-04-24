from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm
from .services import register_user


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = register_user(self.request, form)
        return redirect('pages:home')
