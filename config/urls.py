from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('apps.tests.urls.pages')),
    path('', include('apps.users.urls', namespace='users')),
    path('api/tests/', include('apps.tests.urls.api')),
]

if settings.DEBUG and getattr(settings, "DEBUG_TOOLBAR", False):
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
