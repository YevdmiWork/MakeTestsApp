from django.urls import path
from . import views

app_name = 'users'

auth_urlpatterns = [
    path(
        'register/',
        views.RegisterUser.as_view(),
        name='register',
    ),
    path(
        'login/',
        views.LoginUser.as_view(),
        name='login',
    ),
    path(
        'logout/',
        views.LogoutUser.as_view(),
        name='logout',
    ),
]

profile_urlpatterns = [
    path(
        'profile/<str:username>/',
        views.ProfileUser.as_view(),
        name='profile',
    ),
]
urlpatterns = auth_urlpatterns + profile_urlpatterns
