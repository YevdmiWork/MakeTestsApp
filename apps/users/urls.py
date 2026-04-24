from django.urls import path
from . import views

app_name = 'users'

auth_urlpatterns = [
    path(
        'register/',
        views.RegisterUser.as_view(),
        name='register',
    ),
]

profile_urlpatterns = [
]
urlpatterns = auth_urlpatterns + profile_urlpatterns
