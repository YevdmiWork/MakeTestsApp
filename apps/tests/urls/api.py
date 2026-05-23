from django.urls import path

from ..views import api

app_name = 'api'

urlpatterns = [
    path(
        'test/<int:test_id>/update',
        api.update_test_info,
        name='update_test',
    ),
]
