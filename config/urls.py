from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

handler403 = "users.error_handlers.handler403"
handler404 = "users.error_handlers.handler404"
# handler500 = "users.error_handlers.handler500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("academics.urls", namespace="academics")),
    path("", include("courses.urls")),
    path("", include("users.urls")),
    path("", RedirectView.as_view(permanent=False, url="dashboard/")),
    path("attendances/", include("attendances.urls", namespace="attendances")),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
