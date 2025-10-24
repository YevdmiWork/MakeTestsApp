from django.urls import path
from .views import ProfileUser, LoginUser, RegisterUser, logout_user, UserPasswordChange, PasswordChangeDone

app_name = "users"

urlpatterns = [path('profile/<str:username>/', ProfileUser.as_view(), name='profile'),
               path('login/', LoginUser.as_view(), name='login'),
               path('register/', RegisterUser.as_view(), name='register'),
               path('logout/', logout_user, name='logout'),
               path('password_change/', UserPasswordChange.as_view(), name='password_change'),
               path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
               ]
