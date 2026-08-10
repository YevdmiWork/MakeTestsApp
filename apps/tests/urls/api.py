from django.urls import path

from ..views import api

app_name = 'api'

urlpatterns = [
    path(
        'test/<int:test_id>/update',
        api.update_test_info,
        name='update_test',
    ),

    path(
        'tag/<int:test_id>/add/',
        api.add_tag,
        name='add_tag',
    ),
    path(
        'tag/<int:test_id>/remove/',
        api.remove_tag,
        name='remove_tag',
    ),

    path(
        'question/<int:test_id>/add/',
        api.add_question,
        name='add_question',
    ),
    path(
        'question/<int:question_id>/delete/',
        api.delete_question,
        name='delete_question'
    ),
]
