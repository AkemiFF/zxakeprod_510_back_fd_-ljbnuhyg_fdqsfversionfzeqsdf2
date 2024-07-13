import json
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserEmailSerializerVerify, UserSerializerVerify
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import views, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from .serializers import ClientBanSerializer, InfoUserSerializer
from rest_framework.decorators import api_view
from .serializers import ClientUpdateSerializer
from .models import Client
from rest_framework.status import HTTP_200_OK
from .serializers import ResponsableEtablissementSerializer
from .models import ResponsableEtablissement
from rest_framework import generics
from multiprocessing import AuthenticationError
from django.contrib.auth.hashers import check_password
from imaplib import _Authenticator
from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import UserSerializer, TypeResponsableSerializer, ResponsableEtablissementSerializer, TypeCarteBancaireSerializer, ClientSerializer, UserSerializerVerify
from Accounts.models import TypeResponsable, ResponsableEtablissement, TypeCarteBancaire, Client
from rest_framework.permissions import *
from .permissions import IsClientUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Client

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
@permission_classes([AllowAny])
def fetch_clients_detail(request):
    try:
        clients = Client.objects.all()
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(clients, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_count_client(request):
    try:
        number_client = Client.objects.count()
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({'count': number_client}, status=status.HTTP_200_OK)


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
def client_create_email_info(request):
    serializer = InfoUserSerializer(data=request.data)
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

# accounts/views.py


@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data['email']

            verification_code = get_random_string(
                length=6, allowed_chars='1234567890')

            request.session['verification_code'] = verification_code

            send_mail(
                'Your Verification Code',
                f'Your verification code is {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Verification code sent successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@permission_classes([AllowAny])
class CheckEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            exists = Client.objects.filter(email=email).exists()
            return Response({'exists': exists})
        return Response({'error': 'Email is required'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def client_login_with_email(request):
    serializer = UserEmailSerializerVerify(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        provider_id = serializer.validated_data['emailProviderUid']

        try:
            client = Client.objects.get(
                email=email, emailProviderUid=provider_id)
            refresh = RefreshToken.for_user(client)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })

        except Client.DoesNotExist:
            return Response({'email': ['Vous ne posseder pas encore de compte']}, status=status.HTTP_404_NOT_FOUND)
    else:
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


@permission_classes([AllowAny])
class ResponsableEtablissementListByTypeView(generics.ListAPIView):
    serializer_class = ResponsableEtablissementSerializer

    def get_queryset(self):
        type_id = self.kwargs['type_id']
        return ResponsableEtablissement.objects.filter(type_responsable__id=type_id)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_ban_status(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        if client.ban == True:
            client.ban = False
        elif client.ban == False:
            client.ban = True

    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClientBanSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class AdminCheckAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        is_admin = user.is_superuser

        return Response({'is_admin': is_admin}, status=status.HTTP_200_OK)
