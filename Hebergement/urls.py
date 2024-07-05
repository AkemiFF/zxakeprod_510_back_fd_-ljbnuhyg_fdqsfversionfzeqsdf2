from django.urls import path
from Hebergement import views



urlpatterns = [
    path('images-chambre/', views.ImageChambreListAPIView.as_view(),
         name='images-chambre-list'),
    path('get-hebergement-count/', views.get_count, name='hebergement-count'),
]
