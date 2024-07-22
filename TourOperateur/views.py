# views.py

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import *
from .serializers import *


class TourOperateurDetailView(generics.RetrieveAPIView):
    queryset = TourOperateur.objects.all()
    serializer_class = TourOperateurSerializer


class VoyageDetailView(generics.RetrieveAPIView):
    queryset = Voyage.objects.all()
    serializer_class = VoyageSerializer
    permission_classes = [AllowAny]
