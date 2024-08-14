from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from API.serializers import CustomTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status


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
