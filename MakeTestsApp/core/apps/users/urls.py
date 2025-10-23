from django.urls import path
from .views import ProfileUser, LoginUser, RegisterUser

app_name = "users"

urlpatterns = [path('profile/<str:username>/', ProfileUser.as_view(), name='profile'),
               path('login/', LoginUser.as_view(), name='login'),
               path('register/', RegisterUser.as_view(), name='register'),
               ]
