from django.contrib.auth import login


def register_user(request, form):
    user = form.save(commit=False)
    user.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return user
