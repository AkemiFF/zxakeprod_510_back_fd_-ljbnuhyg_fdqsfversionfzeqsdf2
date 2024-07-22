# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("voyages/<int:pk>/", views.VoyageDetailView.as_view(), name="voyage-detail"),
    path(
        "<int:pk>/",
        views.TourOperateurDetailView.as_view(),
        name="tour-operateur-detail",
    ),
]
