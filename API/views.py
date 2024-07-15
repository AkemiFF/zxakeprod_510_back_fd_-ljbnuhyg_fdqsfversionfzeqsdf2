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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


def get_csrf_token_direct(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_endpoint(request):
    return Response({"message": "Vous êtes autorisé à accéder à l'endpoint admin."})
