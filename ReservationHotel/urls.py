from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Accounts.views import custom_404_view

urlpatterns = [
    path("", view=custom_404_view, name="page"),
    path("api/", include("API.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
