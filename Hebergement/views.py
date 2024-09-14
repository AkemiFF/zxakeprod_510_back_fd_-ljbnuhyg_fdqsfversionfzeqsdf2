from rest_framework import generics
from .models import Hebergement
from .serializers import HebergementSerializer
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from rest_framework.exceptions import NotFound

from API.authentication import CustomJWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from Hebergement.serializers import *
from Hebergement.models import *
from rest_framework.permissions import *
from django.db.models import Min
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Hebergement
from Hebergement.utils import generer_description_hebergement  # type: ignore
from django.conf import settings
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Hebergement
from django.conf import settings
from .utils import generer_description_hebergement

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hebergement, Reservation, Chambre
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation, Hebergement
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from Accounts.permissions import IsResponsable


class AdminHebergementListView(generics.ListAPIView):
    queryset = Hebergement.objects.filter(delete=False)
    serializer_class = ShortHebergementSerializer
    permission_classes = [IsAdminUser]


class DeletedHebergementListView(generics.ListAPIView):
    queryset = Hebergement.objects.filter(delete=True)
    serializer_class = ShortHebergementSerializer
    permission_classes = [IsAdminUser]


class RecentReservationsForHebergementView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            hebergement = Hebergement.objects.get(pk=hebergement_id)

            recent_reservations = Reservation.objects.filter(
                hebergement=hebergement
            ).order_by("-date_debut_reserve")[:6]

            from .serializers import ReservationSerializer

            serializer = ReservationSerializer(recent_reservations, many=True)

            return Response(
                {"recent_reservations": serializer.data}, status=status.HTTP_200_OK
            )

        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )


from django.db.models.functions import ExtractWeekDay
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation, Hebergement


class ClientReservationsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, client_id, hebergement_id):
        try:
            client = Client.objects.get(pk=client_id)
            hebergement = Hebergement.objects.get(pk=hebergement_id)

            reservations = Reservation.objects.filter(
                client_reserve=client, hebergement=hebergement
            )

            reservations_data = []
            for reservation in reservations:
                # Calcul du nombre de nuits
                start_date = reservation.date_debut_reserve
                end_date = reservation.date_fin_reserve
                if start_date and end_date:
                    duration = (end_date - start_date).days
                else:
                    duration = 0

                chambre_data = None
                if reservation.chambre_reserve:
                    chambre = reservation.chambre_reserve
                    # Récupère les images associées à la chambre
                    images = ImageChambre.objects.filter(hebergement_chambre=chambre)
                    images_data = [
                        {
                            "url": image.images.url,
                            "couverture": image.couverture,
                            "legende": image.legende_chambre,
                        }
                        for image in images
                    ]

                    chambre_data = {
                        "id": chambre.id,
                        "nom": chambre.nom_chambre,
                        "prix_par_nuit": chambre.prix_nuit_chambre,
                        "images": images_data,
                    }

                reservations_data.append(
                    {
                        "id": reservation.id,
                        "hebergement": reservation.hebergement.id,
                        "chambre": chambre_data,
                        "date_debut_reserve": reservation.date_debut_reserve,
                        "date_fin_reserve": reservation.date_fin_reserve,
                        "nombre_de_nuits": duration,
                        "prix_total_reserve": reservation.prix_total_reserve,
                        "nombre_personnes_reserve": reservation.nombre_personnes_reserve,
                        "client": {
                            "id": client.id,
                            "nom": client.username,
                            "email": client.email,
                        },
                    }
                )

            return Response(
                {"reservations": reservations_data}, status=status.HTTP_200_OK
            )

        except Client.DoesNotExist:
            return Response(
                {"error": "Client non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )


class ReservationsByDayOfWeekView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            hebergement = Hebergement.objects.get(pk=hebergement_id)

            reservations = Reservation.objects.filter(hebergement=hebergement)

            # Annonce les jours de la semaine
            days_of_week = [
                "Lundi",
                "Mardi",
                "Mercredi",
                "Jeudi",
                "Vendredi",
                "Samedi",
                "Dimanche",
            ]

            reservations_by_day = (
                reservations.annotate(day_of_week=ExtractWeekDay("date_debut_reserve"))
                .values("day_of_week")
                .annotate(total_reservations=Count("id"))
                .order_by("day_of_week")
            )

            reservations_count_by_day = {day: 0 for day in days_of_week}

            for item in reservations_by_day:
                day_index = item["day_of_week"] - 1
                reservations_count_by_day[days_of_week[day_index]] = item[
                    "total_reservations"
                ]

            return Response(
                {"reservations_by_day": reservations_count_by_day},
                status=status.HTTP_200_OK,
            )

        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )


class ReservationCountByMonthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            # Vérifie si l'hébergement existe
            hebergement = Hebergement.objects.get(pk=hebergement_id)

            # Filtre les réservations pour l'hébergement spécifié
            reservations_by_month = (
                Reservation.objects.filter(hebergement=hebergement)
                .annotate(month=TruncMonth("date_debut_reserve"))
                .values("month")
                .annotate(total_reservations=Count("id"))
                .order_by("month")
            )

            return Response(
                {"reservations_by_month": list(reservations_by_month)},
                status=status.HTTP_200_OK,
            )
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )


class HebergementStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            # Vérifie si l'hébergement existe
            hebergement = Hebergement.objects.get(pk=hebergement_id)

            # Compte le nombre de réservations pour cet hébergement
            reservation_count = Reservation.objects.filter(
                hebergement=hebergement
            ).count()

            # Compte le nombre de chambres disponibles pour cet hébergement
            available_chambres_count = HebergementChambre.objects.filter(
                hebergement=hebergement, status=1
            ).count()

            # Calcule le nombre total d'invités pour cet hébergement
            total_guests = (
                Reservation.objects.filter(hebergement=hebergement).aggregate(
                    total_guests=Sum("nombre_personnes_reserve")
                )["total_guests"]
                or 0
            )

            return Response(
                {
                    "booking_count": reservation_count,
                    "available_room_count": available_chambres_count,
                    "total_guests": total_guests,
                },
                status=status.HTTP_200_OK,
            )

        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )


class ClientsAndChambresByHebergementView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            hebergement = Hebergement.objects.get(id=hebergement_id)
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        reservations = Reservation.objects.filter(hebergement=hebergement)
        serializer = ReservationWithClientAndChambreSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HebergementReservationsListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hebergement_id = self.kwargs["hebergement_id"]
        return Reservation.objects.filter(hebergement_id=hebergement_id)


class ReservationsByHebergementView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            hebergement = Hebergement.objects.get(id=hebergement_id)
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        reservations = Reservation.objects.filter(hebergement=hebergement)
        reservations_data = []

        for reservation in reservations:
            # Calculate the number of days and nights
            date_debut = reservation.date_debut_reserve
            date_fin = reservation.date_fin_reserve
            delta = date_fin - date_debut

            days = delta.days
            nights = days - 1 if days > 0 else 0

            # Serialize the reservation data
            serialized_data = ReservationSerializer(reservation).data

            # Add days and nights to the serialized data
            serialized_data["nombre_jours"] = days
            serialized_data["nombre_nuits"] = nights

            reservations_data.append(serialized_data)

        return Response(reservations_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_hebergement_chambre(request, pk):
    try:
        hebergement_chambre = HebergementChambre.objects.get(pk=pk)
        chambre = Chambre.objects.get(id=hebergement_chambre.chambre.pk)

    except HebergementChambre.DoesNotExist:
        return Response(
            {"error": "Hebergement chambre not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = GetChambreSerializer(hebergement_chambre)
    response_data = serializer.data

    images = ImageChambre.objects.filter(hebergement_chambre=hebergement_chambre)
    images_data = []

    for image in images:
        with image.images.open() as img_file:
            image_data = {
                "name": image.images.name,
                "content": base64.b64encode(img_file.read()).decode("utf-8"),
            }
        images_data.append(image_data)

    response_data["type_chambre"] = chambre.type_chambre

    response_data["images"] = images_data
    return JsonResponse(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_chambres_by_hotel(request, hebergement_id):
    try:
        hebergement = Hebergement.objects.get(id=hebergement_id)
    except Hebergement.DoesNotExist:
        return Response(
            {"error": "Hebergement not found"}, status=status.HTTP_404_NOT_FOUND
        )

    chambres = HebergementChambre.objects.filter(hebergement=hebergement)
    serializer = HebergementChambreSerializer(chambres, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_hebergement_chambre(request, id):
    try:
        hebergement_chambre = HebergementChambre.objects.get(id=id)
        images_chambre = ImageChambre.objects.filter(
            hebergement_chambre=hebergement_chambre
        )

        # Delete all related images
        for image in images_chambre:
            image.images.delete()  # This will delete the image file from storage
            image.delete()  # This will delete the image instance from the database

        # Now delete the hebergement_chambre instance
        hebergement_chambre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except HebergementChambre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


import base64
from django.core.files.base import ContentFile


@api_view(["PATCH"])
@permission_classes([AllowAny])
def edit_hebergement_chambre(request, pk):

    try:
        hebergement_chambre = HebergementChambre.objects.get(pk=pk)
    except HebergementChambre.DoesNotExist:
        return Response(
            {"error": "Hebergement chambre not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PATCH":
        accessories = []
        for key in request.data:
            if key.startswith("accessories"):
                accessories.append(int(request.data[key]))

        images_list = []
        for key, value in request.FILES.lists():
            if key.startswith("images"):
                images_list.extend(value)

        serializer_data = {
            key: request.data[key]
            for key in request.data
            if key not in ["images_chambre", "images", "accessoires"]
        }

        serializer_data["images_chambre"] = images_list
        serializer_data["accessoires"] = accessories

        serializer = EditChambreSerializer(
            hebergement_chambre, data=serializer_data, partial=True
        )

        if serializer.is_valid():
            hebergement_chambre = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationsByHebergementView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsResponsable]
    authentication_classes = [CustomJWTAuthentication]

    def get_queryset(self):
        hebergement_id = self.kwargs.get("hebergement_id")
        try:
            hebergement = Hebergement.objects.get(id=hebergement_id)
        except Hebergement.DoesNotExist:
            raise NotFound("Hébergement non trouvé.")

        return Notification.objects.filter(hebergement=hebergement)


@api_view(["PATCH", "GET"])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsResponsable])
def edit_commission(request, pk):
    try:
        hebergement = Hebergement.objects.get(
            pk=pk
        )  # Assuming you want to modify Hebergement, not HebergementChambre
    except Hebergement.DoesNotExist:
        return Response(
            {"error": "Hebergement not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        serializer = EditComissionHebergementSerializer(hebergement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        # Only extract the commission data from the request
        commission_data = {"taux_commission": request.data.get("commission")}

        # Use partial=True to only update the fields provided
        serializer = EditComissionHebergementSerializer(
            hebergement, data=commission_data, partial=True
        )

        if serializer.is_valid():
            hebergement = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_hebergement_chambre(request):
    if request.method == "POST":
        # Extract files and accessories from the request
        files = request.FILES
        accessories = []

        # Correctly handle the extraction of indexed accessories
        for key in request.data:
            if key.startswith(
                "accessories"
            ):  # Handles indexed accessories (e.g., accessories[0], accessories[1])
                accessories.append(int(request.data[key]))

        images_list = []
        for key, value in files.lists():
            if key.startswith("images"):  # Ensure this catches images
                images_list.extend(value)

        # Prepare serializer data excluding accessories and images fields
        serializer_data = {
            key: request.data[key]
            for key in request.data
            if key not in ["images_chambre", "images", "accessoires"]
        }

        serializer_data["images_chambre"] = images_list
        serializer_data["accessoires"] = accessories

        # Validate and save the data using the serializer
        serializer = AjoutChambreSerializer(data=serializer_data)

        if serializer.is_valid():
            hebergement_chambre = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Debug serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generer_description_view(request, hebergement_id):
    hebergement = get_object_or_404(Hebergement, id=hebergement_id)
    localisation = (
        f"{hebergement.localisation.ville}, {hebergement.localisation.adresse}"
        if hebergement.localisation
        else "Non spécifiée"
    )
    accessoires = [
        accessoire.accessoire.nom_accessoire
        for accessoire in hebergement.accessoires.all()
    ]

    hebergement_info = {
        "nom_hebergement": hebergement.nom_hebergement,
        "localisation": localisation,
        "description_hebergement": hebergement.description_hebergement,
        "nombre_etoile_hebergement": hebergement.nombre_etoile_hebergement,
        "type_hebergement": (
            hebergement.type_hebergement.type_name
            if hebergement.type_hebergement
            else "Non spécifié"
        ),
        "accessoires": accessoires,
    }

    api_key = settings.OPENAI_API_KEY
    description = generer_description_hebergement(api_key, hebergement_info)
    print(description)
    return JsonResponse({"description": description})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_hebergement_details(request, hebergement_id):
    try:
        hebergement = Hebergement.objects.get(id=hebergement_id)
        serializer = HebergementSerializerAll(hebergement)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Hebergement.DoesNotExist:
        return Response(
            {"error": "Hebergement not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_chambre_details(request, chambre_id):
    try:
        hebergement_chambre = HebergementChambre.objects.get(id=chambre_id)
        serializer = HebergementChambreSerializer(hebergement_chambre)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except HebergementChambre.DoesNotExist:
        return Response(
            {"error": "HebergementChambre not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class AvisClientsListView(generics.ListAPIView):
    queryset = AvisClients.objects.all()
    serializer_class = AllAvisClientsSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_count(request):
    try:
        number_hebergement = Hebergement.objects.count()
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({"count": number_hebergement}, status=status.HTTP_200_OK)


# (Creer hebergement, visualiser hebergement tout les hebergement, modifier et supprimer hebergement)


@api_view(["POST"])
def like_hebergement(request, hebergement_id):
    try:
        hebergement = Hebergement.objects.get(id=hebergement_id)
    except Hebergement.DoesNotExist:
        return Response(
            {"error": "Hébergement non trouvé"}, status=status.HTTP_404_NOT_FOUND
        )

    user = request.user
    if user in hebergement.likes.all():
        hebergement.likes.remove(user)
        return Response({"message": "Like retiré"}, status=status.HTTP_200_OK)
    else:
        hebergement.likes.add(user)
        return Response({"message": "Like ajouté"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_if_client_liked_hebergement(request, hebergement_id):
    try:
        hebergement = Hebergement.objects.get(id=hebergement_id)
        client = request.user

        if hebergement.likes.filter(id=client.id).exists():
            return Response({"liked": True}, status=status.HTTP_200_OK)
        else:
            return Response({"liked": False}, status=status.HTTP_200_OK)
    except Hebergement.DoesNotExist:
        return Response(
            {"error": "Hébergement non trouvé"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_hebergements(request):
    try:
        all_hebergement = (
            Hebergement.objects.filter(autorisation=True, delete=False)
            .annotate(
                min_prix_nuit_chambre=Min("hebergementchambre__prix_nuit_chambre")
            )
            .order_by("-taux_commission")
        )
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(all_hebergement, many=True)
    return Response({"hebergements": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_accessoire(request):
    all_accessoires = AccessoireHebergement.objects.all()

    serializer = AccessoireHebergementSerializer(all_accessoires, many=True)
    return Response({"hebergements": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_suggestion_hebergements(request):
    try:
        all_hebergement = (
            Hebergement.objects.filter(autorisation=True, delete=False)
            .annotate(
                min_prix_nuit_chambre=Min("hebergementchambre__prix_nuit_chambre"),
                note_moyenne=Avg("avis_hotel__note"),
            )
            .order_by("-note_moyenne", "-taux_commission")[:3]
        )
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SuggestionHebergementSerializer(
        all_hebergement, many=True, context={"request": request}
    )

    return Response({"hebergements": serializer.data}, status=status.HTTP_200_OK)


# Visualiser hebergement selon id


@api_view(["GET"])
def get_id_hebergements(request, hebergement_id):
    try:
        id_hebergement = Hebergement.objects.filter(
            pk=hebergement_id, autorisation=True, delete=False
        )
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(id_hebergement, many=True)
    return Response({"hebergements": serializer.data}, status=status.HTTP_200_OK)


# Visualiser hebergement selon id avec son responsable


@api_view(["GET"])
def get_idresp_hebergements(request, responsable_id):
    try:
        id_hebergement = Hebergement.objects.filter(
            responsable_hebergement=responsable_id
        )
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(id_hebergement, many=True)
    return Response({"hebergements": serializer.data}, status=status.HTTP_200_OK)


# Creer hebergement


@api_view(["POST"])
def create_hebergement(request):
    serializer = HebergementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Modifier hebergement


@api_view(["PUT"])
def update_hebergement(request, hebergement_id):
    try:
        hebergement = Hebergement.objects.get(pk=hebergement_id)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = HebergementSerializer(hebergement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete hebergement


@api_view(["POST"])
@permission_classes([AllowAny])
def create_new_hebergement(request):
    hebergement_data = {
        "nom_hebergement": request.data.get("name"),
        "description_hebergement": "",
        "nombre_etoile_hebergement": request.data.get("rate"),
        "responsable_hebergement": request.data.get("responsable_id"),
        "type_hebergement": request.data.get("accommodationType"),
        "nif": request.data.get("nif"),
        "stat": request.data.get("stat"),
        "autorisation": False,
    }

    # localisation_data = {
    #     "adresse": request.data.get("address"),
    #     "ville": request.data.get("city"),
    #     "latitude": None,
    #     "longitude": None,
    # }

    hebergement_serializer = NewHebergementSerializer(data=hebergement_data)

    if hebergement_serializer.is_valid():
        hebergement = hebergement_serializer.save()
        print(request.data)

        # localisation_data["hebergement_id"] = hebergement.id
        # localisation_serializer = LocalisationSerializer(data=localisation_data)

        # if localisation_serializer.is_valid():
        #     localisation_serializer.save()

        return Response(
            {
                "hebergement": hebergement_serializer.data,
                # "localisation": localisation_serializer.data,
                "id_hebergement": hebergement.id,
            },
            status=status.HTTP_201_CREATED,
        )
        # else:
        #     return Response(
        #         {"localisation_errors": localisation_serializer.errors},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
    else:
        return Response(
            {"hebergement_errors": hebergement_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


from rest_framework.views import APIView


class AddImageChambreView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ImageChambreSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddHebergementImageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        hebergement_id = request.data.get("hebergement")

        if hebergement_id == "undefined" or not hebergement_id:
            return Response(
                {"error": "Invalid or missing hebergement ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        hebergement = Hebergement.objects.get(id=hebergement_id)
        image_list = []

        # Parcourir toutes les clés pour récupérer les fichiers
        for key, image in request.FILES.items():
            if key.startswith("image_"):
                image_instance = HebergementImage(
                    hebergement=hebergement,
                    image=image,
                )
                image_instance.save()
                image_list.append(image_instance)

        serializer = HebergementImageSerializer(image_list, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_hebergement(request, pk):
    try:
        hebergement = Hebergement.objects.get(pk=pk)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    hebergement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Get hrbergementaccessoire selon hebergementt


@api_view(["GET"])
def get_accessoires_hebergement(request, hebergement_id):
    try:
        accessoires = HebergementAccessoire.objects.filter(hebergement=hebergement_id)
    except HebergementAccessoire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementAccessoireSerializer(accessoires, many=True)
    return Response({"accessoires": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_accessoire_hebergement(request, pk):
    try:
        accessoire = AccessoireHebergement.objects.get(pk=pk)
    except AccessoireHebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccessoireHebergementSerializer(accessoire)
    return Response(serializer.data)


@api_view(["POST"])
def create_accessoire_hebergement(request):
    serializer = AccessoireHebergementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_accessoire_hebergement(request, pk):
    try:
        accessoire = AccessoireHebergement.objects.get(pk=pk)
    except AccessoireHebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccessoireHebergementSerializer(accessoire, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_accessoire_hebergement(request, pk):
    try:
        accessoire = AccessoireHebergement.objects.get(pk=pk)
    except AccessoireHebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    accessoire.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_accessoire_chambre(request):
    accessoires = AccessoireChambre.objects.all()
    serializer = AccessoireChambreSerializer(accessoires, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_accessoire_chambre(request):
    serializer = AccessoireChambreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_accessoire_chambre(request, pk):
    try:
        accessoire = AccessoireChambre.objects.get(pk=pk)
    except AccessoireChambre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccessoireChambreSerializer(accessoire, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_accessoire_chambre(request, pk):
    try:
        accessoire = AccessoireChambre.objects.get(pk=pk)
    except AccessoireChambre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    accessoire.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def chambre_personaliser_list(request):
    if request.method == "GET":
        chambre_personaliser = ChambrePersonaliser.objects.all()
        serializer = ChambrePersonaliserSerializer(chambre_personaliser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ChambrePersonaliserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def chambre_personaliser_detail(request, pk):
    try:
        chambre_personaliser = ChambrePersonaliser.objects.get(pk=pk)
    except ChambrePersonaliser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ChambrePersonaliserSerializer(chambre_personaliser)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = ChambrePersonaliserSerializer(
            chambre_personaliser, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        chambre_personaliser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def get_post_chambres(request):
    if request.method == "GET":
        chambres = Chambre.objects.all()
        serializer = ChambreSerializer(chambres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ChambreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def put_delete_chambre(request, pk):
    try:
        chambre = Chambre.objects.get(pk=pk)
    except Chambre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = ChambreSerializer(chambre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        chambre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    from rest_framework import generics


# @permission_classes()
class HebergementListByResponsableView(generics.ListAPIView):
    serializer_class = HebergementSerializer

    def get_queryset(self):
        responsable_id = self.kwargs["responsable_id"]
        return Hebergement.objects.filter(responsable_hebergement__id=responsable_id)


class TypeHebergementListView(generics.ListAPIView):
    queryset = TypeHebergement.objects.all()
    serializer_class = TypeHebergementSerializer
    permission_classes = [AllowAny]


class ChambreListView(generics.ListAPIView):
    queryset = Chambre.objects.all()
    serializer_class = ChambreSerializer
    permission_classes = [AllowAny]


class MinHebergementDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id, *args, **kwargs):
        hebergement = get_object_or_404(Hebergement, id=hebergement_id)
        serializer = MinHebergementSerializer(hebergement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, hebergement_id, *args, **kwargs):
        hebergement = get_object_or_404(Hebergement, id=hebergement_id)
        serializer = MinHebergementSerializer(hebergement, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, hebergement_id, *args, **kwargs):
        hebergement = get_object_or_404(Hebergement, id=hebergement_id)
        data = request.data.copy()

        # Handle localisation update separately
        localisation_data = data.pop("localisation", None)

        if localisation_data:
            localisation = get_object_or_404(
                Localisation, hebergement_id=hebergement.id
            )
            localisation_serializer = LocalisationSerializer(
                localisation, data=localisation_data, partial=True
            )
            if localisation_serializer.is_valid():
                localisation_serializer.save()
            else:
                return Response(
                    localisation_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        # Handle the rest of the hebergement data
        serializer = MinHebergementSerializer(hebergement, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateLocalisationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LocalisationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


StatusSerializer


class ToggleDeleteHebergement(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk, format=None):
        try:
            hebergement = Hebergement.objects.get(pk=pk)
            hebergement.delete = not hebergement.delete
            hebergement.autorisation = not hebergement.autorisation
            hebergement.save()
            return Response({"delete": hebergement.delete}, status=status.HTTP_200_OK)
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hebergement not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ToggleAutorisationView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk, format=None):
        try:
            hebergement = Hebergement.objects.get(pk=pk)
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hebergement not found"}, status=status.HTTP_404_NOT_FOUND
            )

        hebergement.autorisation = not hebergement.autorisation
        hebergement.save()

        serializer = StatusSerializer(hebergement)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.http import JsonResponse
from django.utils.dateparse import parse_date
from .models import HebergementChambre, Reservation


@api_view(["POST"])
@permission_classes([AllowAny])
def check_availability_and_calculate_price(request):
    if request.method == "POST":
        data = request.data
        chambre_details = data.get(
            "chambres", []
        )  # Liste d'objets contenant chambre id et quantité
        check_in = parse_date(data.get("check_in"))
        check_out = parse_date(data.get("check_out"))
        nombre_personnes = data.get("guests", 1)

        if not chambre_details or not check_in or not check_out:
            return JsonResponse({"error": "Invalid data"}, status=400)

        nombre_de_jours = (check_out - check_in).days
        total_price = 0
        unavailable_chambres = []
        reservation_details = []

        for chambre_detail in chambre_details:
            chambre_id = chambre_detail.get("id")
            quantity = chambre_detail.get(
                "quantity", 1
            )  # Quantité de chambres réservées

            try:
                chambre = HebergementChambre.objects.get(id=chambre_id)

                prix_par_nuit = chambre.prix_final()
                prix_par_nuit_arrondi = round(prix_par_nuit, 2)
                prix_total_chambre = (
                    prix_par_nuit_arrondi * nombre_de_jours * quantity
                )  # Multiplie par la quantité

                reservation_exists = Reservation.objects.filter(
                    chambre_reserve=chambre,
                    date_debut_reserve__lt=check_out,
                    date_fin_reserve__gt=check_in,
                    est_validee_reserve=True,
                ).exists()

                if reservation_exists:
                    unavailable_chambres.append(chambre_id)
                else:
                    total_price += prix_total_chambre
                    for _ in range(quantity):
                        reservation_details.append(
                            {
                                "hebergement": chambre.hebergement.id,
                                "chambre_reserve": chambre.id,
                                "date_debut_reserve": check_in,
                                "date_fin_reserve": check_out,
                                "nombre_personnes_reserve": nombre_personnes,
                                "nombre_chambre_reserve": quantity,
                                "prix_total_reserve": prix_total_chambre,
                                "est_validee_reserve": False,
                            }
                        )

            except HebergementChambre.DoesNotExist:
                unavailable_chambres.append(chambre_id)

        if unavailable_chambres:
            return JsonResponse(
                {
                    "unavailable_chambres": unavailable_chambres,
                    "message": "Certaines chambres ne sont pas disponibles pour les dates sélectionnées.",
                },
                status=400,
            )

        return JsonResponse(
            {
                "total_price": total_price,
                "message": "Toutes les chambres sont disponibles.",
                "reservation_details": reservation_details,
            },
            status=200,
        )
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


class CreateTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        # Extraire les données nécessaires du JSON de la requête
        transaction_data = request.data

        # Formater les données pour le modèle Transaction
        formatted_data = {
            "transaction_id": transaction_data.get("id"),
            "status": transaction_data.get("status"),
            "amount": transaction_data["purchase_units"][0]["amount"]["value"],
            "currency": transaction_data["purchase_units"][0]["amount"][
                "currency_code"
            ],
            "payer_name": f"{transaction_data['payer']['name']['given_name']} {transaction_data['payer']['name']['surname']}",
            "payer_email": transaction_data["payer"]["email_address"],
            "payer_id": transaction_data["payer"]["payer_id"],
            "payee_email": transaction_data["purchase_units"][0]["payee"][
                "email_address"
            ],
            "merchant_id": transaction_data["purchase_units"][0]["payee"][
                "merchant_id"
            ],
            "description": transaction_data["purchase_units"][0].get("description"),
            "shipping_address": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["address_line_1"],
            "shipping_city": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["admin_area_2"],
            "shipping_state": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["admin_area_1"],
            "shipping_postal_code": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["postal_code"],
            "shipping_country": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["country_code"],
            "create_time": transaction_data["create_time"],
            "update_time": transaction_data["update_time"],
            "capture_id": transaction_data["purchase_units"][0]["payments"]["captures"][
                0
            ].get("id"),
        }

        # Sérialiser les données
        serializer = TransactionHebergementSerializer(data=formatted_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTransactionHebergementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        transaction_data = request.data

        formatted_data = {
            "transaction_id": transaction_data.get("id"),
            "status": transaction_data.get("status"),
            "amount": transaction_data["purchase_units"][0]["amount"]["value"],
            "currency": transaction_data["purchase_units"][0]["amount"][
                "currency_code"
            ],
            "payer_name": f"{transaction_data['payer']['name']['given_name']} {transaction_data['payer']['name']['surname']}",
            "payer_email": transaction_data["payer"]["email_address"],
            "payer_id": transaction_data["payer"]["payer_id"],
            "payee_email": transaction_data["purchase_units"][0]["payee"][
                "email_address"
            ],
            "merchant_id": transaction_data["purchase_units"][0]["payee"][
                "merchant_id"
            ],
            "description": transaction_data["purchase_units"][0].get("description"),
            "shipping_address": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["address_line_1"],
            "shipping_city": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["admin_area_2"],
            "shipping_state": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["admin_area_1"],
            "shipping_postal_code": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["postal_code"],
            "shipping_country": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["country_code"],
            "create_time": transaction_data["create_time"],
            "update_time": transaction_data["update_time"],
            "capture_id": transaction_data["purchase_units"][0]["payments"]["captures"][
                0
            ].get("id"),
            "client": request.user.id,
        }

        serializer = TransactionHebergementSerializer(data=formatted_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CreateReservationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = ReservationSerializer(data=request.data)
#         if serializer.is_valid():
#             reservation = serializer.save(client_reserve=request.user.client)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_transaction(transaction_data, user):
    formatted_data = {
        "transaction_id": transaction_data.get("id"),
        "status": transaction_data.get("status"),
        "amount": transaction_data["purchase_units"][0]["amount"]["value"],
        "currency": transaction_data["purchase_units"][0]["amount"]["currency_code"],
        "payer_name": f"{transaction_data['payer']['name']['given_name']} {transaction_data['payer']['name']['surname']}",
        "payer_email": transaction_data["payer"]["email_address"],
        "payer_id": transaction_data["payer"]["payer_id"],
        "payee_email": transaction_data["purchase_units"][0]["payee"]["email_address"],
        "merchant_id": transaction_data["purchase_units"][0]["payee"]["merchant_id"],
        "description": transaction_data["purchase_units"][0].get("description"),
        "shipping_address": transaction_data["purchase_units"][0]["shipping"][
            "address"
        ]["address_line_1"],
        "shipping_city": transaction_data["purchase_units"][0]["shipping"]["address"][
            "admin_area_2"
        ],
        "shipping_state": transaction_data["purchase_units"][0]["shipping"]["address"][
            "admin_area_1"
        ],
        "shipping_postal_code": transaction_data["purchase_units"][0]["shipping"][
            "address"
        ]["postal_code"],
        "shipping_country": transaction_data["purchase_units"][0]["shipping"][
            "address"
        ]["country_code"],
        "create_time": transaction_data["create_time"],
        "update_time": transaction_data["update_time"],
        "capture_id": transaction_data["purchase_units"][0]["payments"]["captures"][
            0
        ].get("id"),
        "client": user.id,
    }

    serializer = TransactionHebergementSerializer(data=formatted_data)
    if serializer.is_valid():
        transaction = serializer.save()
        return transaction, None
    return None, serializer.errors


from decimal import Decimal, ROUND_HALF_UP

# class CreateReservationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):

#         reservation_data_list = request.data.get("reservation_data")

#         if not reservation_data_list:
#             return Response(
#                 {"error": "No reservation data provided"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         transaction, errors = create_transaction(
#             request.data.get("transaction"), request.user
#         )

#         if errors:
#             return Response(errors, status=status.HTTP_400_BAD_REQUEST)

#         created_reservations = []

#         for reservation_data in reservation_data_list:

#             reservation_data["client_reserve"] = request.user.id
#             reservation_data["transaction_id"] = transaction.id

#             serializer = ReservationSerializer1(data=reservation_data)
#             if serializer.is_valid():
#                 reservation = serializer.save()
#                 created_reservations.append(serializer.data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#         return Response(created_reservations, status=status.HTTP_201_CREATED)
class CreateReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        reservation_data_list = request.data.get("reservation_data")

        if not reservation_data_list:
            return Response(
                {"error": "No reservation data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Créer une transaction
        transaction, errors = create_transaction(
            request.data.get("transaction"), request.user
        )

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Regrouper les réservations par chambre et hébergement
        grouped_reservations = {}
        for reservation_data in reservation_data_list:
            chambre_id = reservation_data["chambre_reserve"]
            hebergement_id = reservation_data["hebergement"]

            if (chambre_id, hebergement_id) not in grouped_reservations:
                grouped_reservations[(chambre_id, hebergement_id)] = {
                    "chambre_reserve": chambre_id,
                    "hebergement": hebergement_id,
                    "date_debut_reserve": reservation_data["date_debut_reserve"],
                    "date_fin_reserve": reservation_data["date_fin_reserve"],
                    "nombre_chambre_reserve": 0,  # Compter le nombre de chambres
                    "nombre_personnes_reserve": 0,  # Somme des personnes
                    "prix_total_reserve": 0,  # Somme des prix
                    "client_reserve": request.user.id,
                    "transaction": transaction.id,
                }

            # Mise à jour des informations de réservation
            grouped_reservations[(chambre_id, hebergement_id)][
                "nombre_chambre_reserve"
            ] += reservation_data["nombre_chambre_reserve"]
            grouped_reservations[(chambre_id, hebergement_id)][
                "nombre_personnes_reserve"
            ] += reservation_data["nombre_personnes_reserve"]

            # Calculer le prix total (si applicable)
            # Supposons que tu as une fonction pour obtenir le prix par chambre
            chambre = HebergementChambre.objects.get(id=chambre_id)
            prix_par_nuit = chambre.prix_final()
            nombre_de_jours = (
                parse_date(reservation_data["date_fin_reserve"])
                - parse_date(reservation_data["date_debut_reserve"])
            ).days
            prix_total_chambre = prix_par_nuit * nombre_de_jours
            prix_total_chambre_total = (
                prix_total_chambre * reservation_data["nombre_chambre_reserve"]
            )

            grouped_reservations[(chambre_id, hebergement_id)][
                "prix_total_reserve"
            ] += Decimal(prix_total_chambre_total).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        created_reservations = []
        for key, data in grouped_reservations.items():
            serializer = ReservationSerializer1(data=data)
            if serializer.is_valid():
                reservation = serializer.save()
                created_reservations.append(serializer.data)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_reservations, status=status.HTTP_201_CREATED)


class ClientReservationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        client = request.user
        reservations = Reservation.objects.filter(client_reserve=client)
        serializer = ListReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=200)


def get_accommodations_by_city_or_address(request, location):
    accommodations = Hebergement.objects.filter(
        localisation__adresse__icontains=location, autorisation=True, delete=False
    ) | Hebergement.objects.filter(
        localisation__ville__icontains=location, autorisation=True, delete=False
    )

    images = []

    for accommodation in accommodations.distinct():  # Pour éviter les doublons
        for image in accommodation.images.all():
            images.append(
                {
                    "src": image.image.url,
                    "legende": image.legende_hebergement,
                    "couverture": image.couverture,
                }
            )

    return JsonResponse(images, safe=False)


def get_unique_cities(request):
    # Filtrer les hébergements en fonction des critères spécifiés
    hebergements_autorises = Hebergement.objects.filter(autorisation=True, delete=False)

    localisations = (
        Localisation.objects.filter(hebergement_id__in=hebergements_autorises)
        .values_list("ville", flat=True)
        .distinct()
    )

    unique_cities = set(
        localisation.split(" ")[-1] for localisation in localisations if localisation
    )

    return JsonResponse(list(unique_cities), safe=False)


class HebergementImageView(APIView):
    permission_classes = [IsResponsable]
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request, hebergement_id, format=None):
        """
        Retourne toutes les images d'un hébergement spécifié.
        """
        images = HebergementImage.objects.filter(hebergement_id=hebergement_id)
        serializer = HebergementImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, hebergement_id, format=None):
        """
        Crée de nouvelles images pour l'hébergement spécifié.
        """
        files = request.FILES
        # Liste pour stocker les données de réponse après l'enregistrement
        response_data = []

        # Itérer sur tous les fichiers envoyés
        for file in files.values():
            # Créer une instance de HebergementImage pour chaque fichier
            image_instance = HebergementImage(hebergement_id=hebergement_id, image=file)
            image_instance.save()

            # Sérialiser l'image pour la réponse
            serializer = HebergementImageSerializer(image_instance)
            response_data.append(serializer.data)

        # Retourner les données des images nouvellement créées
        return Response(response_data, status=status.HTTP_201_CREATED)

    def delete(self, request, hebergement_id, format=None):
        """
        Supprime toutes les images d'un hébergement spécifié.
        """
        image_ids = request.data.get("image_ids", [])

        if not image_ids:
            return Response(
                {"error": "No image IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        images = HebergementImage.objects.filter(id__in=image_ids)
        count, _ = images.delete()

        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)
