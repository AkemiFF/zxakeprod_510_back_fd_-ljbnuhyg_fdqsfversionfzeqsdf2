from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import TypeResponsableSerializer, ResponsableEtablissementSerializer, TypeCarteBancaireSerializer, ClientSerializer
from Accounts.models import TypeResponsable, ResponsableEtablissement, TypeCarteBancaire, Client
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsClientUser

# Pour la partie TypeResponsable
@api_view(['GET'])
@permission_classes([IsClientUser])
def type_responsable_detail(request, pk):
    try:
        type_responsable = TypeResponsable.objects.get(pk=pk)
    except TypeResponsable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TypeResponsableSerializer(type_responsable)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def type_responsable_create(request):
    serializer = TypeResponsableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def type_responsable_update(request, pk):
    try:
        type_responsable = TypeResponsable.objects.get(pk=pk)
    except TypeResponsable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TypeResponsableSerializer(type_responsable, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def type_responsable_delete(request, pk):
    try:
        type_responsable = TypeResponsable.objects.get(pk=pk)
    except TypeResponsable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    type_responsable.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Pour la partie ResponsableEtablissement
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def responsable_etablissement_detail(request, pk):
    try:
        responsable_etablissement = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ResponsableEtablissementSerializer(responsable_etablissement)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def responsable_etablissement_create(request):
    serializer = ResponsableEtablissementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def responsable_etablissement_update(request, pk):
    try:
        responsable_etablissement = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ResponsableEtablissementSerializer(responsable_etablissement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def responsable_etablissement_delete(request, pk):
    try:
        responsable_etablissement = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    responsable_etablissement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Pour la partie TypeCarteBancaire
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def type_carte_bancaire_detail(request, pk):
    try:
        type_carte_bancaire = TypeCarteBancaire.objects.get(pk=pk)
    except TypeCarteBancaire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TypeCarteBancaireSerializer(type_carte_bancaire)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def type_carte_bancaire_create(request):
    serializer = TypeCarteBancaireSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def type_carte_bancaire_update(request, pk):
    try:
        type_carte_bancaire = TypeCarteBancaire.objects.get(pk=pk)
    except TypeCarteBancaire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TypeCarteBancaireSerializer(type_carte_bancaire, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def type_carte_bancaire_delete(request, pk):
    try:
        type_carte_bancaire = TypeCarteBancaire.objects.get(pk=pk)
    except TypeCarteBancaire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    type_carte_bancaire.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Pour la partie Clients
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fecth_clients_detail(request):
    try:
        client = Client.objects.all()
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def client_create(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def client_update(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def client_delete(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    client.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
