from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from API import views

urlpatterns = [
    path('hebergement/', include('Hebergement.urls')), # Include Hebergements URLs here
    path('admin/', admin.site.urls),
    path('info/', include('Accounts.urls')),
    path('user/', views.user_endpoint, name='user_endpoint'),

    path('artisanal/', include('Artisanal.urls')),  # Include Artisanal URLs here
    path('tourOperateur/', include('TourOperateur.urls')), #Include TourOperateur URLs her

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
