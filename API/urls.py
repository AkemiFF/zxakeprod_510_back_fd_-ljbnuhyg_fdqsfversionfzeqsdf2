from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from API import views
from API.views import *

urlpatterns = [
    path("hebergement/", include("Hebergement.urls")),
    path("accounts/", include("Accounts.urls")),
    path("artisanat/", include("Artisanal.urls")),
    path(
        "week-stats/",
        StatsDerniersJoursAPIView.as_view(),
        name="stats-derniers-jours",
    ),
    path(
        "monthly-stats/",
        StatsDerniersMoisAPIView.as_view(),
        name="stats-derniers-mois",
    ),
    path("stats-counts/", StatsCountsAPIView.as_view(), name="stats-counts"),
    path("chatbot/", include("ChatBot.urls")),
    path("tour/", include("TourOperateur.urls")),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_token"),
    path(
        "get-csrf-token-direct/",
        views.get_csrf_token_direct,
        name="get_csrf_token_direct",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "log/admin/", CustomAdminTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "token-with-email/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair_email",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "token/responsable/",
        ResponsableEtablissementTokenObtainPairView.as_view(),
        name="responsable_token_obtain_pair",
    ),
    path("message/", include("Message.urls")),
    path("secure-endpoint/", MySecureView.as_view(), name="secure_endpoint"),
]
