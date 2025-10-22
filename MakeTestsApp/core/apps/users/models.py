import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
    )
    time_update = models.DateTimeField(
        auto_now=True,
    )
