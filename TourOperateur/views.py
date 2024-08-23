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


class AddTourImageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        tour_id = request.data.get("id")

        if tour_id == "undefined" or not tour_id:
            return Response(
                {"error": "Invalid or missing hebergement ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tour = TourOperateur.objects.get(id=tour_id)
        image_list = []

        # Parcourir toutes les clés pour récupérer les fichiers
        for key, image in request.FILES.items():
            if key.startswith("image_"):
                image_instance = ImageTour(
                    images_tour=tour,
                    image=image,
                )
                image_instance.save()
                image_list.append(image_instance)

        serializer = ImageTourSerializer(image_list, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class CheckVoyageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        booking_info = request.data

        id_voyage = booking_info.get("id_voyage")
        nb_voyageur = booking_info.get("nb_voyageur")

        # Vérification des données envoyées
        if not id_voyage or not nb_voyageur:
            return Response(
                {"error": "Voyage ID and number of voyageurs are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Récupérer le voyage correspondant
        try:
            voyage = Voyage.objects.get(id=id_voyage)
        except Voyage.DoesNotExist:
            return Response(
                {"error": "Voyage not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Vérifier la disponibilité des places
        if voyage.places_disponibles < nb_voyageur:
            return Response(
                {"error": "Not enough places available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculer le prix total
        prix_total = voyage.prix_voyage * nb_voyageur

        # Renvoyer les informations vérifiées
        return Response(
            {
                "voyage": voyage.id,
                "prix_voyage": voyage.prix_voyage,
                "prix_total": prix_total,
                "places_disponibles": voyage.places_disponibles,
                "nombre_voyageurs": nb_voyageur,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )


class TourOperateurViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

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


class ReservationDeVoyageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        reservation_data = request.data.get("reservation_data")
        if not reservation_data:
            return Response(
                {"error": "No reservation data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction_data = request.data.get("transaction")
        if not transaction_data:
            return Response(
                {"error": "No transaction data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction, errors = create_transaction_tour(transaction_data, request.user)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        reservation_data["client"] = request.user.id
        reservation_data["transaction"] = transaction.id

        serializer = CreateReservationVoyageSerializer(data=reservation_data)
        if serializer.is_valid():
            reservation = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_transaction_tour(transaction_data, user):
    try:
        formatted_data = {
            "transaction_id": transaction_data.get("id", ""),
            "status": transaction_data.get("status", ""),
            "amount": transaction_data["purchase_units"][0]["amount"]["value"],
            "currency": transaction_data["purchase_units"][0]["amount"][
                "currency_code"
            ],
            "payer_name": f"{transaction_data['payer']['name']['given_name']} {transaction_data['payer']['name']['surname']}",
            "payer_email": transaction_data["payer"]["email_address"],
            "payer_id": transaction_data["payer"]["payer_id"],
            "payee_email": transaction_data["purchase_units"][0]["payee"][
                "email_address"
            ],
            "merchant_id": transaction_data["purchase_units"][0]["payee"][
                "merchant_id"
            ],
            "description": transaction_data["purchase_units"][0].get("description", ""),
            "shipping_address": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["address_line_1"],
            "shipping_city": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["admin_area_2"],
            "shipping_state": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["admin_area_1"],
            "shipping_postal_code": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["postal_code"],
            "shipping_country": transaction_data["purchase_units"][0]["shipping"][
                "address"
            ]["country_code"],
            "create_time": transaction_data["create_time"],
            "update_time": transaction_data["update_time"],
            "capture_id": transaction_data["purchase_units"][0]["payments"]["captures"][
                0
            ].get("id", ""),
            "client": user.id,
        }

        serializer = TransactionTourSerializer(data=formatted_data)

        if serializer.is_valid():
            transaction = serializer.save()
            print(serializer.data)
            return transaction, None
        else:
            return None, serializer.errors

    except KeyError as e:
        return None, {"error": f"Missing data: {str(e)}"}
    except Exception as e:
        return None, {"error": str(e)}
