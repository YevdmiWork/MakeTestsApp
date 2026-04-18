from django.urls import path
from ..views import pages

app_name = 'pages'

urlpatterns = [
    path(
        'tests/',
        pages.AllTests.as_view(),
        name='home',
    ),
]
