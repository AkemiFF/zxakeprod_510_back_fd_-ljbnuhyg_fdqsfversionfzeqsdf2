from Accounts.views import custom_404_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("", custom_404_view, name="page"),
    path("api/", include("API.urls")),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Serve static files in production only if absolutely necessary (e.g., custom use cases)
    urlpatterns.append(
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    )