# urls.py

from django.urls import path
from .views import VoyageListView, VoyageDetailView
from . import views

urlpatterns = [
    path("voyages/<int:pk>/", views.VoyageDetailView.as_view(), name="voyage-detail"),
    path("voyages/", views.VoyageListView.as_view(), name="voyage-list"),
    path(
        "get_all_tour_operateurs/",
        views.TourOperateurListCreateView.as_view(),
        name="tour_operateur-list-create",
    ),
    path(
        "get_id_tour_operateurs/<int:pk>/",
        views.TourOperateurDetailView.as_view(),
        name="tour_operateur-detail",
    ),
    path("voyages/", views.get_all_voyages, name="get_all_voyages"),
    path("voyages-populaire/", views.get_popular_voyages, name="get_popular_voyages"),
    path(
        "operateurs-populaires/",
        views.get_popular_tour_operateurs,
        name="get_popular_tour_operateurs",
    ),
    path(
        "<int:pk>/voyages/",
        views.TourOperateurViewSet.as_view({"get": "voyages"}),
        name="tour-operateur-voyages",
    ),
]
