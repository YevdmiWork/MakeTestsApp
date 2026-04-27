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
    path(
        'password_change/',
        views.UserPasswordChange.as_view(),
        name='password_change',
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDone.as_view(),
        name='password_change_done',
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
