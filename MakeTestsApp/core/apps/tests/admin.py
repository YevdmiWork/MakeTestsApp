from django.contrib import admin
from .forms import TestAdminForm
from .models import Test, Tag


class TestAdmin(admin.ModelAdmin):
    form = TestAdminForm
    filter_horizontal = ('tag',)

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


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Test, TestAdmin)
admin.site.register(Tag, TagAdmin)
