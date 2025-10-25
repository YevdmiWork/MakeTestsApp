from django.contrib import admin
from .forms import TestAdminForm
from .models import Test, Tag
from .services import generate_unique_slug

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    form = TestAdminForm
    list_display_links = (
        'title',
    )
    list_display = (
        'title',
    )
    search_fields = (
        'title',
        'author__username',
        'slug',
    )
    readonly_fields = (
        'slug',
        'time_create',
        'time_update',
        'author',
    )
    list_filter = (
        'time_create',
        'time_update',
        'author',
    )
    filter_horizontal = (
        'tag',
    )

    def save_model(
            self,
            request,
            test_instance: Test,
            form,
            change: bool,
            ):
        if not test_instance.slug:
            test_instance.slug = generate_unique_slug()
        test_instance.author = request.user
        super().save_model(request, test_instance, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    list_display_links = (
        'id',
        'name'
    )
