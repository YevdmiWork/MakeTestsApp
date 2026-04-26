from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

User = get_user_model()

class ProfileTestsMixin:
    @cached_property
    def profile_user(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )
