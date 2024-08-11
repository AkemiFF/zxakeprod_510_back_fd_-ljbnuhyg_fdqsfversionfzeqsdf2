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

from django.db.models import Sum
from rest_framework.views import APIView
from django.db.models import Count, Func
from django.utils import timezone


class TourOperateurCreateView(generics.CreateAPIView):
    queryset = TourOperateur.objects.all()
    serializer_class = CreateTourOperateurSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_localisation_tour(request):
    if request.method == "POST":
        serializer = LocalisationTourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_images_to_voyage(request, voyage_id):
    try:
        voyage = Voyage.objects.get(id=voyage_id)
    except Voyage.DoesNotExist:
        return Response({"error": "Voyage not found"}, status=status.HTTP_404_NOT_FOUND)

    images = request.FILES.getlist("images")

    if not images:
        return Response(
            {"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    for image in images:
        image_voyage = ImageVoyage.objects.create(image_voyage=voyage, image=image)
        if (
            ImageVoyage.objects.filter(image_voyage=voyage, couverture=True).count()
            == 0
        ):
            image_voyage.couverture = True
            image_voyage.save()

    return Response(
        {"success": "Images added successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def create_voyage(request):
    serializer = CreateVoyageSerializer(data=request.data)
    if serializer.is_valid():
        voyage = serializer.save()
        return Response(
            CreateVoyageSerializer(voyage).data, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def list_voyages(request, pk):
    try:
        tour_operateur = TourOperateur.objects.get(pk=pk)
        voyages = Voyage.objects.filter(tour_operateur=tour_operateur)
        serializer = ListVoyageSerializer(voyages, many=True)
        return Response(serializer.data)
    except TourOperateur.DoesNotExist:
        return Response(
            {"detail": "Tour Operateur not found."}, status=status.HTTP_404_NOT_FOUND
        )


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


@api_view(["PATCH"])
@permission_classes([AllowAny])
def update_voyage(request, pk):
    try:
        voyage = Voyage.objects.get(pk=pk)
        serializer = ListVoyageSerializer(voyage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Voyage.DoesNotExist:
        return Response(
            {"detail": "Voyage not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def create_trajet_voyage(request, voyage_id):
    try:
        # Vérifie que le voyage existe
        voyage = Voyage.objects.get(pk=voyage_id)

        # Crée une copie des données de la requête
        data = request.data.copy()

        # Ajoute l'ID du voyage aux données
        data["voyage"] = voyage.id

        # Sérialise et valide les données
        serializer = ShortTrajetVoyageSerializer(data=data)

        if serializer.is_valid():
            # Sauvegarde si les données sont valides
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Voyage.DoesNotExist:
        return Response(
            {"detail": "Voyage not found."}, status=status.HTTP_404_NOT_FOUND
        )


class TypeInclusionListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = TypeInclusion.objects.all()
    serializer_class = TypeInclusionSerializer


class TourOperateurStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tour_operateur_id):
        try:
            tour_operateur = TourOperateur.objects.get(pk=tour_operateur_id)

            voyage_count = Voyage.objects.filter(tour_operateur=tour_operateur).count()

            reservation_count = ReservationVoyage.objects.filter(
                voyage__tour_operateur=tour_operateur
            ).count()

            total_guests = (
                ReservationVoyage.objects.filter(
                    voyage__tour_operateur=tour_operateur
                ).aggregate(total_guests=Sum("nombre_voyageurs"))["total_guests"]
                or 0
            )

            return Response(
                {
                    "voyage_count": voyage_count,
                    "booking_count": reservation_count,
                    "total_guests": total_guests,
                },
                status=status.HTTP_200_OK,
            )

        except TourOperateur.DoesNotExist:
            return Response(
                {"error": "Tour opérateur non trouvé."},
                status=status.HTTP_404_NOT_FOUND,
            )


from django.db.models.functions import ExtractMonth


class MonthlyReservationStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tour_operateur_id):
        try:
            tour_operateur = TourOperateur.objects.get(pk=tour_operateur_id)

            year = request.query_params.get("year", timezone.now().year)

            reservations = ReservationVoyage.objects.filter(
                voyage__tour_operateur=tour_operateur,
                date_reservation_voyage__year=year,
            )

            monthly_reservations = (
                reservations.annotate(month=ExtractMonth("date_reservation_voyage"))
                .values("month")
                .annotate(total_reservations=Count("id"))
                .order_by("month")
            )

            monthly_stats = {month: 0 for month in range(1, 13)}

            for entry in monthly_reservations:
                month = entry["month"]
                total_reservations = entry["total_reservations"]
                monthly_stats[month] = total_reservations

            return Response(
                {"year": year, "monthly_reservations": monthly_stats},
                status=status.HTTP_200_OK,
            )

        except TourOperateur.DoesNotExist:
            return Response(
                {"error": "Tour opérateur non trouvé."},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_recent_reservations_for_tour_operateur(request, tour_operateur_id):
    try:
        tour_operateur = TourOperateur.objects.get(pk=tour_operateur_id)

        recent_reservations = ReservationVoyage.objects.filter(
            voyage__tour_operateur=tour_operateur
        ).order_by("-date_reservation_voyage")[:6]

        serializer = ReservationVoyageSerializer(recent_reservations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except TourOperateur.DoesNotExist:
        return Response(
            {"error": "Tour opérateur non trouvé."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
