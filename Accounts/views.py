from django.shortcuts import render
from templated_email import send_templated_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
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
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .models import Client, VerificationCode, ResponsableEtablissement
from rest_framework.status import HTTP_200_OK
from .serializers import *
from rest_framework import generics
from django.contrib.auth.hashers import check_password
from imaplib import _Authenticator
from django.http import JsonResponse
from rest_framework.response import Response

from Accounts.models import (
    TypeResponsable,
    ResponsableEtablissement,
    TypeCarteBancaire,
    Client,
)
from rest_framework.permissions import *
from .permissions import IsClientUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate


class ResponsableLoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email et mot de passe sont requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = ResponsableEtablissement.objects.get(email=email)
        except ResponsableEtablissement.DoesNotExist:
            return Response(
                {"error": "Identifiants invalides ou utilisateur non autorisé"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Vérifier le mot de passe
        if not user.check_password(password):
            return Response(
                {"error": "Identifiants invalides ou utilisateur non autorisé"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Générer les tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "refresh": str(refresh),
                "access": str(access),
                "user": ResponsableEtablissementSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class ResponsableEtablissementDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, responsable_id):
        try:
            responsable = ResponsableEtablissement.objects.get(id=responsable_id)
        except ResponsableEtablissement.DoesNotExist:
            return Response(
                {"error": "Responsable non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResponsableEtablissementSerializer(responsable)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, responsable_id):
        try:
            responsable = ResponsableEtablissement.objects.get(id=responsable_id)
        except ResponsableEtablissement.DoesNotExist:
            return Response(
                {"error": "Responsable non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResponsableEtablissementSerializer(
            responsable, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def custom_404_view(request, exception=None):
    return render(request, "404.html")


class ResponsableEtablissementCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddResponsableEtablissementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsClientUser])
def type_responsable_detail(request, pk):
    try:
        type_responsable = TypeResponsable.objects.get(pk=pk)
    except TypeResponsable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TypeResponsableSerializer(type_responsable)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def type_responsable_create(request):
    serializer = TypeResponsableSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
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


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def type_responsable_delete(request, pk):
    try:
        type_responsable = TypeResponsable.objects.get(pk=pk)
    except TypeResponsable.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    type_responsable.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Pour la partie ResponsableEtablissement
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def responsable_etablissement_detail(request, pk):
    try:
        responsable_etablissement = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ResponsableEtablissementSerializer(responsable_etablissement)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def responsable_etablissement_create(request):
    serializer = ResponsableEtablissementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
def responsable_etablissement_update(request, pk):
    try:
        responsable_etablissement = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ResponsableEtablissementSerializer(
        responsable_etablissement, data=request.data
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def responsable_etablissement_delete(request, pk):
    try:
        responsable_etablissement = ResponsableEtablissement.objects.get(pk=pk)
    except ResponsableEtablissement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    responsable_etablissement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Pour la partie TypeCarteBancaire
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def type_carte_bancaire_detail(request, pk):
    try:
        type_carte_bancaire = TypeCarteBancaire.objects.get(pk=pk)
    except TypeCarteBancaire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TypeCarteBancaireSerializer(type_carte_bancaire)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def type_carte_bancaire_create(request):
    serializer = TypeCarteBancaireSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
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


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def type_carte_bancaire_delete(request, pk):
    try:
        type_carte_bancaire = TypeCarteBancaire.objects.get(pk=pk)
    except TypeCarteBancaire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    type_carte_bancaire.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Pour la partie Clients
@api_view(["GET"])
@permission_classes([AllowAny])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profil_client(request):
    try:
        client = request.user
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client)
    return Response(serializer.data)


# Get all customer lists


@api_view(["GET"])
@permission_classes([AllowAny])
def fetch_clients_detail(request):
    try:
        clients = Client.objects.all()
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(clients, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def get_count_client(request):
    try:
        number_client = Client.objects.count()
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response({"count": number_client}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def client_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access_token),
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def client_create_email_info(request):
    if request.method == "POST":
        serializer = ClientWithEmailSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()

            refresh = RefreshToken.for_user(client)
            access_token = refresh.access_token

            return Response(
                {
                    "id": client.id,
                    "username": client.username,
                    "email": client.email,
                    "refresh": str(refresh),
                    "access": str(access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def create_client_with_email(request):
#     if request.method == "POST":
#         serializer = ClientWithEmailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_client_with_email(request):
    if request.method == "POST":
        serializer = ClientWithEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response_data = {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access_token),
                "emailPhotoUrl": user.emailPhotoUrl,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@permission_classes([AllowAny])
def reset_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            code = data.get("code")

            if not email or not password:
                return JsonResponse(
                    {"error": "Email and password are required."}, status=400
                )
            verification_code = VerificationCode.objects.filter(
                user_email=email, code=code
            ).first()

            try:
                if verification_code:
                    user = Client.objects.get(email=email)
                    user.password = make_password(password)
                    user.save()

                    verification_code.delete()

                    return JsonResponse(
                        {"success": "Password reset successfully."}, status=200
                    )
                else:
                    JsonResponse({"error": "Please try again"}, status=401)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "User does not exist."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@api_view(["POST"])
@permission_classes([AllowAny])
def client_login(request):
    serializer = UserSerializerVerify(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            client = Client.objects.get(email=email)
            if check_password(password, client.password):
                refresh = RefreshToken.for_user(client)

                profil_pic_url = (
                    request.build_absolute_uri(client.profilPic.url)
                    if client.profilPic
                    else None
                )

                return Response(
                    {
                        "message": "Login successful",
                        "id": client.id,
                        "username": client.username,
                        "image": profil_pic_url,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            else:
                return Response(
                    {"password": ["Mot de passe incorrect"]},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Client.DoesNotExist:
            return Response(
                {"email": ["Email incorrect ou n'existe pas"]},
                status=status.HTTP_404_NOT_FOUND,
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# accounts/views.py


@csrf_exempt
def send_verification_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data["email"]

            verification_code = get_random_string(length=6, allowed_chars="1234567890")

            VerificationCode.objects.create(user_email=email, code=verification_code)

            context = {
                "verification_code": verification_code,
                "user_name": email,
                "link_token": "aftrip.com",
                "type_action": "signup to aftrip",
            }

            html_message = render_to_string("email/verification.html", context=context)

            send_mail(
                "Your Verification Code",
                "",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_message,
            )

            return JsonResponse(
                {"message": "Verification code sent successfully"}, status=200
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def welcome_mail(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data["email"]
            context = {
                "user_name": email,
                "link_token": "aftrip.com",
                "type_action": "signup to aftrip",
                "host": settings.FRONT_HOST,
            }

            html_message = render_to_string("email/welcome.html", context=context)
            client = Client.objects.get(email=email)

            send_mail(
                "Welcome to Aftrip",
                "",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_message,
            )

            return JsonResponse(
                {"message": "Verification code sent successfully", "id": client.id},
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def send_recovery_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data["email"]

            verification_code = get_random_string(length=6, allowed_chars="1234567890")

            VerificationCode.objects.create(user_email=email, code=verification_code)

            context = {
                "verification_code": verification_code,
                "user_name": email,
                "link_token": "aftrip.com",
                "type_action": "recover password",
            }

            html_message = render_to_string("email/verification.html", context=context)

            x = send_mail(
                "Your Verification Code",
                "",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_message,
            )
            print(x)
            return JsonResponse(
                {"message": "Verification code sent successfully"}, status=200
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def verify_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data["email"]
            code = data["code"]

            if not email or not code:
                return JsonResponse(
                    {"error": "Email and code are required"}, status=400
                )

            verification_code = VerificationCode.objects.filter(
                user_email=email, code=code
            ).first()

            if verification_code and not verification_code.IsUsed():
                verification_code.used = True
                verification_code.save()
                return JsonResponse({"message": "Verification successful"}, status=200)
            else:
                return JsonResponse(
                    {"error": "Invalid or expired verification code"}, status=400
                )
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@permission_classes([AllowAny])
class CheckEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if email:
            exists = Client.objects.filter(email=email).exists()
            return Response({"exists": exists})
        return Response({"error": "Email is required"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def client_login_with_email(request):
    serializer = UserEmailSerializerVerify(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        try:
            client = Client.objects.get(email=email)
            refresh = RefreshToken.for_user(client)
            return Response(
                {
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "id": client.id,
                    "profilPic": (client.profilPic.url if client.profilPic else None),
                    "username": client.username,
                }
            )

        except Client.DoesNotExist:
            return Response(
                {"email": ["Vous ne posseder pas encore de compte"]},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def client_login(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#     user = AuthenticationError(email=email, password=password)

#     if user is not None:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#         })

#     return Response({
#         'email': ['Email incorrect ou n\'existe pas.'],
#         'password': ['Mot de passe incorrect.'],
#     }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
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


@api_view(["DELETE"])
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
        type_id = self.kwargs["type_id"]
        return ResponsableEtablissement.objects.filter(type_responsable__id=type_id)


@api_view(["PATCH"])
@permission_classes([AllowAny])
def update_ban_status(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        if client.ban == True:
            client.ban = False
        elif client.ban == False:
            client.ban = True

    except Client.DoesNotExist:
        return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

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

        return Response({"is_admin": is_admin}, status=status.HTTP_200_OK)


class EditClientView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = EditClientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Client.objects.get(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
