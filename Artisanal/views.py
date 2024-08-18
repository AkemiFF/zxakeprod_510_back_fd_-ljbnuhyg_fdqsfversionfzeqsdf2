from rest_framework import viewsets, permissions, generics, status
from .models import Artisanat, ProduitArtisanal, Panier, ItemPanier, Commande
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from django.db.models import Count


class SpecificationListView(generics.ListAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [AllowAny]


class CreateImageProduitArtisanalView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist("image[]")
        produit_id = request.data.get("produit")

        if not images:
            return Response(
                {"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        created_images = []
        for image in images:
            data = {"produit": produit_id, "image": image}
            serializer = ImageProduitSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created_images.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_images, status=status.HTTP_201_CREATED)


class ProduitArtisanalDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk, format=None):
        try:
            produit = ProduitArtisanal.objects.get(pk=pk)
            produit.delete()
            return Response(
                {"detail": "Produit supprimé avec succès."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ProduitArtisanal.DoesNotExist:
            return Response(
                {"detail": "Produit non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )


class ToggleAutorisationView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk, format=None):
        try:
            artisanat = Artisanat.objects.get(pk=pk)
        except Artisanat.DoesNotExist:
            return Response(
                {"error": "Hebergement not found"}, status=status.HTTP_404_NOT_FOUND
            )

        artisanat.active = not artisanat.active
        artisanat.save()

        serializer = ArtisanatSerializer(artisanat)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtisanatListView(generics.ListAPIView):
    queryset = Artisanat.objects.all()
    serializer_class = ArtisanatSerializer
    permission_classes = [IsAdminUser]


class ProduitArtisanalListView(generics.ListCreateAPIView):
    serializer_class = FieldsProduitArtisanalSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        artisanat_id = self.kwargs["artisanat_id"]
        return ProduitArtisanal.objects.filter(artisanat_id=artisanat_id)

    def put(self, request, *args, **kwargs):
        try:
            product = ProduitArtisanal.objects.get(pk=kwargs["pk"])
        except ProduitArtisanal.DoesNotExist:
            return Response(
                {"error": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = FieldsProduitArtisanalSerializer(
            product, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommandeDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Commande.objects.all()
    serializer_class = DetailCommandeSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        try:
            commande = self.queryset.get(pk=pk)
        except Commande.DoesNotExist:
            return Response(
                {"detail": "Commande not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(commande)
        return Response(serializer.data)


class ArtisanatCommandesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, artisanat_id):
        try:
            artisanat_products = ProduitArtisanal.objects.filter(
                artisanat_id=artisanat_id, itempanier__panier__commande__isnull=False
            ).distinct()
            serializer = ArtisanatCommandeSerializer(artisanat_products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProduitArtisanal.DoesNotExist:
            return Response(
                {"error": "Artisanat not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PanierView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            panier = Panier.objects.get(client=request.user)
            serializer = PanierSerializer(panier)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Panier.DoesNotExist:
            return Response(
                {"error": "Panier non trouvé pour ce client."},
                status=status.HTTP_404_NOT_FOUND,
            )


class ClientsByArtisanatView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, artisanat_id):
        try:
            artisanat = Artisanat.objects.get(id=artisanat_id)
        except Artisanat.DoesNotExist:
            return Response(
                {"detail": "Artisanat not found"}, status=status.HTTP_404_NOT_FOUND
            )

        commandes = Commande.objects.filter(
            panier__produits__artisanat=artisanat
        ).distinct()
        clients = Client.objects.filter(commandes__in=commandes).distinct()

        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class ArtisanatViewSet(viewsets.ModelViewSet):
    queryset = Artisanat.objects.all()
    serializer_class = ArtisanatDetailSerializer
    permission_classes = [permissions.AllowAny]


class ArtisanatCreateView(generics.CreateAPIView):
    queryset = Artisanat.objects.all()
    serializer_class = ArtisanatSerializer
    permission_classes = [permissions.AllowAny]


class ProduitArtisanalViewSet(viewsets.ModelViewSet):
    queryset = ProduitArtisanal.objects.all()
    serializer_class = ProduitArtisanalSerializer
    permission_classes = [permissions.AllowAny]


class FiltreLikeProduitArtisanalViewSet(viewsets.ModelViewSet):
    serializer_class = ProduitArtisanalSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = ProduitArtisanal.objects.annotate(total_likes=Count("likes"))
        queryset = queryset.order_by("-total_likes")[:6]
        return queryset


class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    permission_classes = [permissions.AllowAny]


class ItemPanierViewSet(viewsets.ModelViewSet):
    queryset = ItemPanier.objects.all()
    serializer_class = ItemPanierSerializer
    permission_classes = [permissions.AllowAny]


class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.AllowAny]


class ProduitArtisanalDetailView(generics.RetrieveAPIView):
    queryset = ProduitArtisanal.objects.all()
    serializer_class = ProduitArtisanalDetailSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    user = request.user
    produit_id = request.data.get("produit_id")
    quantite = request.data.get("quantite", 1)

    try:
        produit = ProduitArtisanal.objects.get(id=produit_id)
    except ProduitArtisanal.DoesNotExist:
        return Response(
            {"error": "Produit non trouvé."}, status=status.HTTP_404_NOT_FOUND
        )

    panier, created = Panier.objects.get_or_create(client=user)

    item, item_created = ItemPanier.objects.get_or_create(
        panier=panier, produit=produit
    )

    if not item_created:
        item.quantite += quantite
    else:
        item.quantite = quantite

    item.save()

    serializer = ItemPanierSerializer(item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def check_if_client_liked_product(request, produit_id):
    try:
        produit = ProduitArtisanal.objects.get(id=produit_id)
        client = request.user

        if produit.likes.filter(id=client.id).exists():
            return Response({"liked": True}, status=status.HTTP_200_OK)
        else:
            return Response({"liked": False}, status=status.HTTP_200_OK)
    except ProduitArtisanal.DoesNotExist:
        return Response(
            {"error": "Produit not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def like_produit(request, produit_id):
    try:
        produit = ProduitArtisanal.objects.get(id=produit_id)
    except ProduitArtisanal.DoesNotExist:
        return Response(
            {"error": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND
        )

    user = request.user
    if user in produit.likes.all():
        produit.likes.remove(user)
        return Response({"message": "Like retiré"}, status=status.HTTP_200_OK)
    else:
        produit.likes.add(user)
        return Response({"message": "Like ajouté"}, status=status.HTTP_200_OK)


from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def filter_produits(request):
    specifications = request.data.get("specifications", [])

    if not specifications:
        return Response(
            {"error": "No specifications provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    spec_ids = [spec["id"] for spec in specifications if "id" in spec]

    produits = ProduitArtisanal.objects.filter(
        specifications__id__in=spec_ids
    ).distinct()

    serializer = ProduitArtisanalSerializer(produits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
