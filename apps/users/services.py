from django.contrib.auth import login
from django.db import transaction


def register_user(request, form):
    with transaction.atomic():
        user = form.save()
        login(request, user)
    return user
