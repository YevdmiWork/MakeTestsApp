from django.urls import path

from ..views import pages

app_name = 'pages'

urlpatterns = [
    path(
        'tests/',
        pages.AllTests.as_view(),
        name='home',
    ),
    path(
        'tests/create',
        pages.AddTest.as_view(),
        name='create',
    ),
    path(
        'tests/<slug:test_slug>/edit/',
        pages.TestEdit.as_view(),
        name='edit',
    ),
]
