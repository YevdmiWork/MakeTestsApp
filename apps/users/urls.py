from django.urls import path
from . import views

app_name = 'users'

auth_urlpatterns = [
]

profile_urlpatterns = [
]

urlpatterns = auth_urlpatterns + profile_urlpatterns
