from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from Hebergement.serializers import HebergementSerializer, HebergementAccessoireSerializer, AccessoireHebergementSerializer, AccessoireChambreSerializer, HebergementChambreSerializer
from Hebergement.models import Hebergement, HebergementAccessoire, AccessoireHebergement, HebergementChambre, AccessoireChambre
from rest_framework.permissions import IsAdminUser, IsAuthenticated

@api_view(['GET'])
def get_count(request):
    try:
        number_hebergement = Hebergement.objects.count()
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_hebergement}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_hebergements(request):
    try:
        all_hebergement = Hebergement.objects.all()
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementSerializer(all_hebergement, many=True)
    return Response({'hebergements': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_hebergement(request):
    serializer = HebergementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_hebergement(request, pk):
    try:
        hebergement = Hebergement.objects.get(pk=pk)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = HebergementSerializer(hebergement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_hebergement(request, pk):
    try:
        hebergement = Hebergement.objects.get(pk=pk)
    except Hebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    hebergement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_hebergement_accessoires(request, hebergement_id):
    try:
        accessoires = HebergementAccessoire.objects.filter(hebergement_id=hebergement_id)
    except HebergementAccessoire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementAccessoireSerializer(accessoires, many=True)
    return Response({'accessoires': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_hebergement_accessoires_all(request):
    try:
        accessoires = HebergementAccessoire.objects.all()
    except HebergementAccessoire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = HebergementAccessoireSerializer(accessoires, many=True)
    return Response({'accessoires': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def accessoire_hebergement_list(request):
    if request.method == 'GET':
        accessoires = AccessoireHebergement.objects.all()
        serializer = AccessoireHebergementSerializer(accessoires, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AccessoireHebergementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def accessoire_hebergement_detail(request, pk):
    try:
        accessoire = AccessoireHebergement.objects.get(pk=pk)
    except AccessoireHebergement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccessoireHebergementSerializer(accessoire)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AccessoireHebergementSerializer(accessoire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        accessoire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def hebergement_chambre_list(request, hebergement_id):
    if request.method == 'GET':
        hebergement_chambres = HebergementChambre.objects.filter(hebergement_id=hebergement_id)
        serializer = HebergementChambreSerializer(hebergement_chambres, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = HebergementChambreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def hebergement_chambre_detail(request, hebergement_id, chambre_id):
    try:
        hebergement_chambre = HebergementChambre.objects.get(hebergement_id=hebergement_id, id=chambre_id)
    except HebergementChambre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HebergementChambreSerializer(hebergement_chambre)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HebergementChambreSerializer(hebergement_chambre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hebergement_chambre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def accessoire_chambre_list(request):
    accessoires = AccessoireChambre.objects.all()
    serializer = AccessoireChambreSerializer(accessoires, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def accessoire_chambre_create(request):
    serializer = AccessoireChambreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def accessoire_chambre_detail(request, pk):
    try:
        accessoire = AccessoireChambre.objects.get(pk=pk)
    except AccessoireChambre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccessoireChambreSerializer(accessoire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        accessoire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import serializers
from .models import Chambre

class ChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chambre
        fields = '__all__'

@api_view(['GET'])
def chambre_list(request):
    chambres = Chambre.objects.all()
    serializer = ChambreSerializer(chambres, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def chambre_create(request):
    serializer = ChambreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def chambre_detail(request, pk):
    try:
        chambre = Chambre.objects.get(pk=pk)
    except Chambre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ChambreSerializer(chambre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        chambre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import serializers
from .models import HebergementAccessoire

class HebergementAccessoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementAccessoire
        fields = '__all__'

@api_view(['GET'])
def hebergement_accessoire_list(request):
    hebergement_accessoires = HebergementAccessoire.objects.all()
    serializer = HebergementAccessoireSerializer(hebergement_accessoires, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def hebergement_accessoire_create(request):
    serializer = HebergementAccessoireSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def hebergement_accessoire_detail(request, pk):
    try:
        hebergement_accessoire = HebergementAccessoire.objects.get(pk=pk)
    except HebergementAccessoire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = HebergementAccessoireSerializer(hebergement_accessoire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hebergement_accessoire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import serializers
from .models import HebergementChambreAccessoire

class HebergementChambreAccessoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebergementChambreAccessoire
        fields = '__all__'

@api_view(['GET'])
def hebergement_chambre_accessoire_list(request):
    hebergement_chambre_accessoires = HebergementChambreAccessoire.objects.all()
    serializer = HebergementChambreAccessoireSerializer(hebergement_chambre_accessoires, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def hebergement_chambre_accessoire_create(request):
    serializer = HebergementChambreAccessoireSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def hebergement_chambre_accessoire_detail(request, pk):
    try:
        hebergement_chambre_accessoire = HebergementChambreAccessoire.objects.get(pk=pk)
    except HebergementChambreAccessoire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = HebergementChambreAccessoireSerializer(hebergement_chambre_accessoire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hebergement_chambre_accessoire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
