from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore
from API import views

urlpatterns = [
    path('hebergement/', include('Hebergement.urls')),
    path('info/', include('Accounts.urls')),
    path('user/', views.user_endpoint, name='user_endpoint'),
    path('artisanal/', include('Artisanal.urls')),
    path('tourOperateur/', include('TourOperateur.urls')),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
