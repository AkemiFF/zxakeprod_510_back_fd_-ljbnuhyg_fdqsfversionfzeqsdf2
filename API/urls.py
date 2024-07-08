from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore
from API import views

urlpatterns = [
    # Include Hebergements URLs here
    path('hebergement/', include('Hebergement.urls')),
    path('info/', include('Accounts.urls')),
    path('user/', views.user_endpoint, name='user_endpoint'),

    # Include Artisanal URLs here
    path('artisanal/', include('Artisanal.urls')),
    # Include TourOperateur URLs her
    path('tourOperateur/', include('TourOperateur.urls')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
