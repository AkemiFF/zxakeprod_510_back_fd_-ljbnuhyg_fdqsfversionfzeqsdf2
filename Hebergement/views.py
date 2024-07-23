from rest_framework import generics
from .models import Hebergement
from .serializers import HebergementSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from Hebergement.serializers import *
from Hebergement.models import (
    Chambre,
    Hebergement,
    HebergementAccessoire,
    AccessoireHebergement,
    AccessoireChambre,
    ChambrePersonaliser,
)
from rest_framework.permissions import *
from django.db.models import Min
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Hebergement
from Hebergement.utils import generer_description_hebergement  # type: ignore
from django.conf import settings


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
        "type_hebergement": hebergement.type_hebergement.type_name,
        "accessoires": accessoires,
    }

    api_key = settings.OPENAI_API_KEY
    description = generer_description_hebergement(api_key, hebergement_info)

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
