from django.contrib import admin
from .models import Test


class TestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'time_create',
        'time_update',
        'content',
        'slug',
        'author',
        'rating',
        'completion',
    )

    list_display_links = (
        'id',
        'title',
        'time_create',
        'time_update',
        'content',
        'slug',
        'author',
        'rating',
        'completion',
    )


admin.site.register(Test, TestAdmin)
