# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Tour Operateur URLs
    path('tour_operateurs/', views.get_all_tour_operateurs, name='tour-operateurs-list'),
    path('tour_operateurs/<int:pk>/', views.get_tour_operateur_by_id, name='tour-operateur-detail'),
    path('tour_operateurs/<int:pk>/voyages/', views.get_tour_operateur_voyages, name='tour-operateur-voyages'),

    # Voyage URLs
    path('voyages/', views.get_all_voyages, name='voyages-list'),
    path('voyages/<int:pk>/', views.get_voyage_by_id, name='voyage-detail'),
    path('voyages/<int:pk>/images/', views.get_voyage_images, name='voyage-images'),

    # Reservation Voyage URLs
    path('reservations/', views.get_all_reservations, name='reservations-list'),
    path('reservations/<int:pk>/', views.get_reservation_by_id, name='reservation-detail'),
    path('reservations/create/', views.create_reservation, name='reservation-create'),
    path('reservations/<int:pk>/', views.reservation_detail, name='reservation-detail'),
]
