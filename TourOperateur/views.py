# views.py


from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import *
from .serializers import *
from .models import Voyage
from .serializers import VoyageSerializer


class TourOperateurViewSet(viewsets.ViewSet):
    @action(detail=True, methods=["get"])
    def voyages(self, request, pk=None):
        try:
            tour_operateur = TourOperateur.objects.get(pk=pk)
        except TourOperateur.DoesNotExist:
            return Response({"error": "Tour opérateur non trouvé"}, status=404)

        voyages = Voyage.objects.filter(tour_operateur=tour_operateur)
        serializer = ShortVoyageSerializer(voyages, many=True)
        return Response(serializer.data)


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
