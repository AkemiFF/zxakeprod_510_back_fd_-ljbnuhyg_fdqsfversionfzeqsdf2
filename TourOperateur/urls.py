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
    path("voyages/", views.get_all_voyages, name="get_all_voyages"),
    path("voyages-populaire/", views.get_popular_voyages, name="get_popular_voyages"),
    path(
        "operateurs-populaires/",
        views.get_popular_tour_operateurs,
        name="get_popular_tour_operateurs",
    ),
]
