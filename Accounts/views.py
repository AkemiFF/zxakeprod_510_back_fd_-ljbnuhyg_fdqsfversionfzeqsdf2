from multiprocessing import AuthenticationError
from django.contrib.auth.hashers import check_password
from imaplib import _Authenticator
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer, TypeResponsableSerializer, ResponsableEtablissementSerializer, TypeCarteBancaireSerializer, ClientSerializer, UserSerializerVerify
from Accounts.models import TypeResponsable, ResponsableEtablissement, TypeCarteBancaire, Client
from rest_framework.permissions import *
from .permissions import IsClientUser
from rest_framework_simplejwt.tokens import RefreshToken

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

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

    serializer = ResponsableEtablissementSerializer(
        responsable_etablissement, data=request.data)
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

    serializer = TypeCarteBancaireSerializer(
        type_carte_bancaire, data=request.data)
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
@permission_classes([AllowAny])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client)
    return Response(serializer.data)

# Get all customer lists


@api_view(['GET'])
@permission_classes([IsAdminUser])
def fetch_clients_detail(request):
    try:
        clients = Client.objects.all()
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(clients, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([AllowAny])
def client_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def client_login(request):
    serializer = UserSerializerVerify(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            client = Client.objects.get(email=email)
            if check_password(password, client.password):
                refresh = RefreshToken.for_user(client)
                return Response({'message': 'Login successful', 'refresh': str(refresh), 'access': str(refresh.access_token)})
            else:
                return Response({'password': ['Mot de passe incorrect']}, status=status.HTTP_401_UNAUTHORIZED)
        except Client.DoesNotExist:
            return Response({'email': ['Email incorrect ou n\'existe pas']}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def client_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = AuthenticationError(email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

    return Response({
        'email': ['Email incorrect ou n\'existe pas.'],
        'password': ['Mot de passe incorrect.'],
    }, status=status.HTTP_400_BAD_REQUEST)


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
