from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from API import views

urlpatterns = [
    path('hebergement/', include('Hebergement.urls')),
    path('accounts/', include('Accounts.urls')),
    path('user/', views.user_endpoint, name='user_endpoint'),
    path('artisanal/', include('Artisanal.urls')),
    path('tourOperateur/', include('TourOperateur.urls')),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('get-csrf-token-direct/',
         views.get_csrf_token_direct, name='get_csrf_token_direct'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
