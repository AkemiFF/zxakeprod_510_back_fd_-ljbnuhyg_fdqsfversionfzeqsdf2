from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from API.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from .authentication import CustomJWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase
from Accounts.models import Client, ResponsableEtablissement
from Accounts.permissions import *
from django.utils import timezone
from rest_framework import status
from datetime import timedelta
from Hebergement.models import Reservation
from Artisanal.models import Artisanat, CommandeProduit
from TourOperateur.models import ReservationVoyage, TourOperateur
from django.utils import timezone
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


class StatsCountsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Compter les instances de chaque modèle
        tour_operateur_count = TourOperateur.objects.count()
        hebergement_count = Hebergement.objects.count()
        artisanat_count = Artisanat.objects.count()

        # Préparer les données à retourner
        data = {
            "nombre_tour_operateur": tour_operateur_count,
            "nombre_hebergement": hebergement_count,
            "nombre_artisanat": artisanat_count,
        }

        return Response(data, status=status.HTTP_200_OK)


class StatsDerniersMoisAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Calculer le mois courant et les 7 derniers mois
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        seven_months_ago = first_day_of_current_month - relativedelta(months=6)

        # Initialiser les listes pour stocker les statistiques mensuelles
        reservations_hebergement = []
        achats_produits_artisanaux = []
        reservations_voyages = []
        mois = []

        for i in range(7):
            start_month = seven_months_ago + relativedelta(months=i)
            next_month = start_month + relativedelta(months=1)

            # Rendre les dates conscientes du fuseau horaire
            start_month_aware = timezone.make_aware(
                dt.combine(start_month, dt.min.time())
            )
            next_month_aware = timezone.make_aware(
                dt.combine(next_month, dt.min.time())
            )

            # Ajouter les statistiques pour chaque mois
            reservations_hebergement.append(
                Reservation.objects.filter(
                    created_at__gte=start_month_aware,
                    created_at__lt=next_month_aware,
                ).count()
            )
            achats_produits_artisanaux.append(
                CommandeProduit.objects.filter(
                    date_commande__gte=start_month_aware,
                    date_commande__lt=next_month_aware,
                ).count()
            )
            reservations_voyages.append(
                ReservationVoyage.objects.filter(
                    date_reservation_voyage__gte=start_month_aware,
                    date_reservation_voyage__lt=next_month_aware,
                ).count()
            )

            # Ajouter le nom du mois
            mois.append(start_month.strftime("%B"))

        data = {
            "reservations_hebergement": reservations_hebergement,
            "achats_produits_artisanaux": achats_produits_artisanaux,
            "reservations_voyages": reservations_voyages,
            "derniers_mois": mois,
        }

        return Response(data, status=status.HTTP_200_OK)


class StatsDerniersJoursAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Calculer la date d'il y a 7 jours
        today = timezone.now().date()
        last_week = today - timedelta(days=6)

        # Initialiser les listes pour stocker les statistiques quotidiennes
        reservations_hebergement = []
        achats_produits_artisanaux = []
        reservations_voyages = []
        jours = []

        for i in range(7):
            day = last_week + timedelta(days=i)
            next_day = day + timedelta(days=1)

            start_day_aware = timezone.make_aware(dt.combine(day, dt.min.time()))
            next_day_aware = timezone.make_aware(dt.combine(next_day, dt.min.time()))

            # Ajouter les statistiques pour chaque jour
            reservations_hebergement.append(
                Reservation.objects.filter(
                    created_at__gte=day, created_at__lt=next_day
                ).count()
            )
            achats_produits_artisanaux.append(
                CommandeProduit.objects.filter(
                    date_commande__gte=day, date_commande__lt=next_day
                ).count()
            )
            reservations_voyages.append(
                ReservationVoyage.objects.filter(
                    date_reservation_voyage__gte=day,
                    date_reservation_voyage__lt=next_day,
                ).count()
            )

            # Ajouter le nom du jour
            jours.append(day.strftime("%A"))

        data = {
            "reservations_hebergement": reservations_hebergement,
            "achats_produits_artisanaux": achats_produits_artisanaux,
            "reservations_voyages": reservations_voyages,
            "derniers_jours": jours,
        }

        return Response(data, status=status.HTTP_200_OK)


class ResponsableEtablissementTokenObtainPairView(TokenViewBase):
    serializer_class = ResponsableEtablissementTokenObtainPairSerializer


class MySecureView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsResponsable]

    def get(self, request):
        # Créez un dictionnaire avec les informations de l'utilisateur
        user_info = {
            "username": request.user.username,
            "email": request.user.email,
            "is_client": isinstance(request.user, Client),
            "is_responsable": isinstance(request.user, ResponsableEtablissement),
        }

        # Retourne une réponse JSON
        return Response({"message": "Vous êtes authentifié!", "user": user_info})


class CustomAdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        user = self.get_user(request.data)

        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # "first_name": user.first_name,
            # "last_name": user.last_name,
            "is_admin": user.is_staff or user.is_superuser,
        }
        if user.is_staff or user.is_superuser:
            response.data["is_admin"] = True
            response.data["user"] = user_info
        else:
            response.data["is_admin"] = False

        return response

    def get_user(self, data):
        """
        Helper method to retrieve the user object based on the request data.
        """
        from django.contrib.auth import authenticate

        user = authenticate(username=data.get("email"), password=data.get("password"))
        return user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})


def get_csrf_token_direct(request):
    token = get_token(request)
    return JsonResponse({"csrfToken": token})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_endpoint(request):
    return Response({"message": "Vous êtes autorisé à accéder à l'endpoint admin."})
