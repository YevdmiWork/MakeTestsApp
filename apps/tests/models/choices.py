from django.db import models


class TestStatus(models.TextChoices):
    PUBLISHED = 'published', 'Опубликовано'
    UNPUBLISHED = 'unpublished', 'Не опубликовано'
