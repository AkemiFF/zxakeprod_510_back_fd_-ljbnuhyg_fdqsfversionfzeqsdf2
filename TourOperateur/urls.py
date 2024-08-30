# urls.py

from django.urls import include, path
from .views import VoyageListView, VoyageDetailView
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path(
        "client/reservations/",
        views.ClientReservationsListView.as_view(),
        name="client-reservations-list",
    ),
    path(
        "add-image/",
        views.AddTourImageView.as_view(),
        name="add-tour-image",
    ),
    path(
        "<int:pk>/list-voyages/",
        views.list_voyages,
        name="list-voyages",
    ),
    path(
        "voyages/<int:voyage_id>/add-images/",
        views.add_images_to_voyage,
        name="add-images-to-voyage",
    ),
    path(
        "transactions/create/",
        views.ReservationDeVoyageView.as_view(),
        name="reservation-de-voyage",
    ),
    path("voyages/create/", views.create_voyage, name="create-voyage"),
    # Route pour mettre à jour les informations d'un voyage spécifique
    path("voyages/<int:pk>/update-voyage/", views.update_voyage, name="update-voyage"),
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
    path("voyage/check/", views.CheckVoyageView.as_view(), name="voyage_check_voyages"),
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
    path(
        "voyages/<int:voyage_id>/create-trajet/",
        views.create_trajet_voyage,
        name="create-trajet-voyage",
    ),
    path(
        "inclusions/", views.TypeInclusionListView.as_view(), name="type-inclusion-list"
    ),
    path(
        "<int:tour_operateur_id>/stats/",
        views.TourOperateurStatsView.as_view(),
        name="tour-operateur-stats",
    ),
    path(
        "<int:tour_operateur_id>/monthly-reservations/",
        views.MonthlyReservationStatsView.as_view(),
        name="monthly-reservations",
    ),
    path(
        "<int:tour_operateur_id>/recent-reservations/",
        views.get_recent_reservations_for_tour_operateur,
        name="recent-reservations",
    ),
    path(
        "create/",
        views.TourOperateurCreateView.as_view(),
        name="create-tour-operateur",
    ),
    path(
        "localisation/create/",
        views.create_localisation_tour,
        name="create_localisation_tour",
    ),
]
