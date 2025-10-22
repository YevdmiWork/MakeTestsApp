from django.urls import path
from django.conf import settings

from .views import AddTest, AllTests, TestView, TestEdit, TestRun

app_name = "tests"

urlpatterns = [path('tests/', AllTests.as_view(), name='home'),
               path('add_test/', AddTest.as_view(), name='add_test'),
               path('tests/<slug:test_slug>/', TestView.as_view(), name='test_view'),
               path('tests/<slug:test_slug>/edit/', TestEdit.as_view(), name='test_edit'),
               path('tests/<slug:test_slug>/run/', TestRun.as_view(), name='test_run'),
               ]
