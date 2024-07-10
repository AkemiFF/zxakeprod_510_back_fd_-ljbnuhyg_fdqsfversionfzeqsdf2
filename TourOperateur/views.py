# views.py

from rest_framework import generics
from .serializers import TourOperateurSerializer
from .models import TourOperateur
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import TourOperateur, Voyage, ImageVoyage, Reservation_voyage
from rest_framework.permissions import *
from .serializers import (
    TourOperateurSerializer,
    VoyageSerializer,
    ImageVoyageSerializer,
    ReservationVoyageSerializer,
)


# Tour Operateur Views

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_tour_operateurs(request):
    try:
        tour_operateurs = TourOperateur.objects.all()
    except TourOperateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TourOperateurSerializer(tour_operateurs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tour_operateur_by_id(request, pk):
    try:
        tour_operateur = TourOperateur.objects.get(pk=pk)
    except TourOperateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TourOperateurSerializer(tour_operateur)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tour_operateur_voyages(request, pk):
    try:
        voyages = Voyage.objects.filter(tour_operateur=pk)
    except Voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = VoyageSerializer(voyages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Voyage Views


@api_view(['GET'])
def get_all_voyages(request):
    try:
        voyages = Voyage.objects.all()
    except Voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = VoyageSerializer(voyages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_voyage_by_id(request, pk):
    try:
        voyage = Voyage.objects.get(pk=pk)
    except Voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = VoyageSerializer(voyage)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_voyage_images(request, pk):
    try:
        images = ImageVoyage.objects.filter(voyage=pk)
    except ImageVoyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ImageVoyageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Reservation Voyage Views


@api_view(['GET'])
def get_all_reservations(request):
    try:
        reservations = Reservation_voyage.objects.all()
    except Reservation_voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReservationVoyageSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


8


@api_view(['GET'])
def get_reservation_by_id(request, pk):
    try:
        reservation = Reservation_voyage.objects.get(pk=pk)
    except Reservation_voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReservationVoyageSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_reservation(request):
    serializer = ReservationVoyageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def reservation_detail(request, pk):
    try:
        reservation = Reservation_voyage.objects.get(pk=pk)
    except Reservation_voyage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ReservationVoyageSerializer(
            reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TourOperateurListByResponsableView(generics.ListAPIView):
    serializer_class = TourOperateurSerializer

    def get_queryset(self):
        responsable_id = self.kwargs['responsable_id']
        return TourOperateur.objects.filter(responsable_TourOperateur__id=responsable_id)
