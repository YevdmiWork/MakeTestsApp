from django.contrib import admin
from django.urls import path, include
from MakeTestsApp.core.project import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]

if settings.DEBUG and getattr(settings, "DEBUG_TOOLBAR", False):
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
