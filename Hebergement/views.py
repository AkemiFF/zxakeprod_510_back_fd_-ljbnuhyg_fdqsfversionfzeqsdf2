from rest_framework import generics
from .models import Hebergement
from .serializers import HebergementSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from Hebergement.serializers import *
from Hebergement.models import *
from django.http import FileResponse

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
import os
from Accounts.permissions import IsResponsableEtablissement
from Accounts.serializers import ResponsableEtablissementSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class ClientsAndChambresByHebergementView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            hebergement = Hebergement.objects.get(id=hebergement_id)
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        reservations = Reservation.objects.filter(hotel_reserve=hebergement)
        serializer = ReservationWithClientAndChambreSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HebergementReservationsListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        hebergement_id = self.kwargs["hebergement_id"]
        return Reservation.objects.filter(hotel_reserve_id=hebergement_id)


class ReservationsByHebergementView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, hebergement_id):
        try:
            hebergement = Hebergement.objects.get(id=hebergement_id)
        except Hebergement.DoesNotExist:
            return Response(
                {"error": "Hébergement non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        reservations = Reservation.objects.filter(hotel_reserve=hebergement)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


@api_view(["PUT"])
@permission_classes([AllowAny])
def edit_hebergement_chambre(request, pk):
    print(request.data)
    try:
        hebergement_chambre = HebergementChambre.objects.get(pk=pk)
    except HebergementChambre.DoesNotExist:
        return Response(
            {"error": "Hebergement chambre not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PUT":
        accessories = []
        for key in request.data:
            if key.startswith("accessories"):
                accessories.append(int(request.data[key]))

        images_list = []
        for key, value in request.data.items():
            if key.startswith("images_chambre"):
                # Assuming the front sends base64 encoded images
                format, imgstr = value.split(";base64,")
                ext = format.split("/")[-1]
                img_data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
                images_list.append(img_data)

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


@api_view(["POST"])
@permission_classes([AllowAny])
def add_hebergement_chambre(request):
    if request.method == "POST":
        # Extract files and accessories from the request
        files = request.FILES

        accessories = []
        for key in request.data:
            if key.startswith("accessories"):
                accessories.append(int(request.data[key]))

        images_list = []
        for key, value in files.lists():
            images_list.extend(value)

        serializer_data = {
            key: request.data[key]
            for key in request.data
            if key not in ["images_chambre", "images", "accessoires"]
        }

        serializer_data["images_chambre"] = images_list
        serializer_data["accessoires"] = accessories

        # Logging instead of print statements

        serializer = AjoutChambreSerializer(data=serializer_data)

        if serializer.is_valid():
            hebergement_chambre = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        all_hebergement = Hebergement.objects.annotate(
            min_prix_nuit_chambre=Min("hebergementchambre__prix_nuit_chambre")
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
        all_hebergement = Hebergement.objects.annotate(
            min_prix_nuit_chambre=Min("hebergementchambre__prix_nuit_chambre"),
            note_moyenne=Avg("avis_hotel__note"),
        ).order_by("-note_moyenne")[:3]
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
        id_hebergement = Hebergement.objects.filter(pk=hebergement_id)
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
    print(hebergement_data)

    localisation_data = {
        "adresse": request.data.get("address"),
        "ville": request.data.get("city"),
        "latitude": None,
        "longitude": None,
    }

    hebergement_serializer = NewHebergementSerializer(data=hebergement_data)

    if hebergement_serializer.is_valid():
        hebergement = hebergement_serializer.save()
        print(request.data)

        localisation_data["hebergement_id"] = hebergement.id
        localisation_serializer = LocalisationSerializer(data=localisation_data)

        if localisation_serializer.is_valid():
            localisation_serializer.save()

            return Response(
                {
                    "hebergement": hebergement_serializer.data,
                    "localisation": localisation_serializer.data,
                    "id_hebergement": hebergement.id,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"localisation_errors": localisation_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        serializer = MinHebergementSerializer(
            hebergement, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
