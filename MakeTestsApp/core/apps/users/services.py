from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .models import User
from ..tests.models import Test


def register_user(request, form):
    user = form.save(commit=False)
    user.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return user


def get_user_tests(username: str):
    get_object_or_404(User, username=username)
    return (
        Test.objects.by_author_username(username)
        .only('id', 'slug', 'time_create', 'title', 'author_id', 'rating', 'completion', 'status')
    )
