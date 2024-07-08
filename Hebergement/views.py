from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from Hebergement.serializers import HebergementAccessoireSerializer, HebergementSerializer
from Hebergement.models import Hebergement, HebergementAccessoire
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Nombre hebergement creer
@api_view(['GET'])
def get_count(request):
    try:
        number_hebergement = Hebergement.objects.count()
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_hebergement}, status=status.HTTP_200_OK)

# (Creer hebergement, visualiser hebergement tout les hebergement, modifier et supprimer hebergement)
@api_view(['GET'])
def get_all_hebergements(request):
    try:
        all_hebergement = Hebergement.objects.all()
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(all_hebergement, many=True)
    return Response({'hebergements': serializer.data}, status=status.HTTP_200_OK)

# Visualiser hebergement selon id
@api_view(['GET'])
def get_id_hebergements(request, hebergement_id):
    try:
        id_hebergement = Hebergement.objects.filter(pk=hebergement_id)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(id_hebergement, many=True)
    return Response({'hebergements': serializer.data}, status=status.HTTP_200_OK)

# Visualiser hebergement selon id avec son responsable
@api_view(['GET'])
def get_idresp_hebergements(request, responsable_id):
    try:
        id_hebergement = Hebergement.objects.filter(responsable_hebergement=responsable_id)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(id_hebergement, many=True)
    return Response({'hebergements': serializer.data}, status=status.HTTP_200_OK)

# Creer hebergement
@api_view(['POST'])
def create_hebergement(request):
    serializer = HebergementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Modifier hebergement
@api_view(['PUT'])
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
@api_view(['DELETE'])
def delete_hebergement(request, pk):
    try:
        hebergement = Hebergement.objects.get(pk=pk)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    hebergement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Get hrbergementaccessoire selon hebergementt
@api_view(['GET'])
def get_accessoires_hebergement(request, hebergement_id):
    try:
        accessoires = HebergementAccessoire.objects.filter(hebergement=hebergement_id)
    except HebergementAccessoire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementAccessoireSerializer(accessoires, many=True)
    return Response({'accessoires': serializer.data}, status=status.HTTP_200_OK)
