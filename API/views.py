from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_endpoint(request):
    return Response({"message": "Vous êtes autorisé à accéder à l'endpoint admin."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_endpoint(request):
    return Response({"message": "Vous êtes autorisé à accéder à l'endpoint utilisateur."})
