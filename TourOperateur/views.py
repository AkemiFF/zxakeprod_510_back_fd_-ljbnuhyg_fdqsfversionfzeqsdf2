# views.py

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import *
from .serializers import *
from .models import Voyage
from .serializers import VoyageSerializer


class TourOperateurListCreateView(generics.ListCreateAPIView):
    queryset = TourOperateur.objects.all()
    serializer_class = TourOperateurSerializer
    permission_classes = [AllowAny]

class TourOperateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourOperateur.objects.all()
    serializer_class = TourOperateurSerializer
    permission_classes = [AllowAny]


class VoyageDetailView(generics.RetrieveAPIView):
    queryset = Voyage.objects.all()
    serializer_class = VoyageSerializer
    permission_classes = [AllowAny]
    

class VoyageListView(generics.ListAPIView):
    queryset = Voyage.objects.all()
    serializer_class = VoyageListSerializer
    permission_classes = [AllowAny]




@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_voyages(request):
    voyages = Voyage.objects.all()
    serializer = AllVoyageSerializer(voyages, many=True)
    return Response(serializer.data)


from django.db.models import Count


@api_view(["GET"])
@permission_classes([AllowAny])
def get_popular_voyages(request):
    voyages = Voyage.objects.annotate(like_count=Count("likes")).order_by(
        "-like_count"
    )[:4]
    serializer = PopularVoyageSerializer(voyages, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_popular_tour_operateurs(request):
    tour_operateurs = TourOperateur.objects.annotate(
        nombre_avis=Count("avis_tour_operateur")
    ).order_by("-nombre_avis")

    serializer = TourOperateurSerializer(tour_operateurs, many=True)
    return Response(serializer.data)
