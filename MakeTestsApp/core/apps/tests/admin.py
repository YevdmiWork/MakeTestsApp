from django.contrib import admin
from .forms import TestAdminForm
from .models import Test, Tag, Question, Answer
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
        'name',
    )
    list_display_links = (
        'id',
        'name',
    )


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    min_num = 2
    max_num = 10
    fields = (
        'text',
        'flag'
    )
    show_change_link = True
    validate_min = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'test',
        'text',
        'type',
    )
    list_display_links = (
        'id',
        'text'
    )
    list_filter = (
        'test',
        'type'
    )
    search_fields = (
        'text',
    )
    ordering = (
        'id',
    )
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'text',
        'flag',
    )
    list_display_links = (
        'id',
        'text'
    )
    list_filter = (
        'flag',
        'question__test'
    )
    search_fields = (
        'text',
        'question__text'
    )
    ordering = (
        'id',
    )
