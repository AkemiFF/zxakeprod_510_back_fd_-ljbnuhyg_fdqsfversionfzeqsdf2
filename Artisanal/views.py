from rest_framework import viewsets, permissions, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from .models import Commande
from .serializers import CommandeProduitSerializer
from .models import Client, ProduitArtisanal, Commande
from .serializers import ClientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# ViewSets


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def LocalisationArtisanatViewSet(request, artisanat_id=None):
    if artisanat_id is not None:
        queryset = LocalisationArtisanat.objects.filter(id=artisanat_id)
        if not queryset.exists():
            return Response(
                {"Aucun responsable trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = LocalisationArtisanatSerializer(queryset, many=True)
        return Response(serializer.data)
    return Response(
        {"error": "Responsable ID non fourni"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def ResponsableEtablissementViewSet(request, artisanat_id=None):
    if artisanat_id is not None:
        queryset = ResponsableEtablissement.objects.filter(id=artisanat_id)
        if not queryset.exists():
            return Response(
                {"Aucun responsable trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResponsableEtablissementSerializer(queryset, many=True)
        return Response(serializer.data)
    return Response(
        {"error": "Responsable ID non fourni"}, status=status.HTTP_400_BAD_REQUEST
    )


@permission_classes([permissions.IsAuthenticated])
class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer
    permission_classes = [permissions.AllowAny]


@permission_classes([permissions.IsAuthenticated])
class ItemPanierViewSet(viewsets.ModelViewSet):
    queryset = ItemPanier.objects.all()
    serializer_class = ItemPanierSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def artisanantList(request, artisanat_id=None):
    if artisanat_id is not None:
        queryset = Artisanat.objects.filter(id=artisanat_id)
        if not queryset.exists():
            return Response(
                {"Aucune artisanat trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ArtisanatSerializer(queryset, many=True)
        return Response(serializer.data)
    return Response(
        {"error": "Artisanat ID non fourni"}, status=status.HTTP_400_BAD_REQUEST
    )


@permission_classes([permissions.IsAuthenticated])
class ArtisanatViewSet(viewsets.ModelViewSet):
    queryset = Artisanat.objects.all()
    serializer_class = ArtisanatDetailSerializer
    permission_classes = [permissions.AllowAny]


@permission_classes([permissions.IsAuthenticated])
class ProduitArtisanalViewSet(viewsets.ModelViewSet):
    serializer_class = ProduitArtisanalSerializer

    def get_queryset(self):
        artisanat_id = self.kwargs.get("artisanat_id")
        # Filtre les produits par artisanat
        return ProduitArtisanal.objects.filter(artisanat_id=artisanat_id)


# @permission_classes([permissions.IsAuthenticated])
# class CommandeProduitViewSet(viewsets.ModelViewSet):
#    queryset = Commande.objects.all()
#    serializer_class = CommandeProduitSerializer
#    permission_classes = [permissions.AllowAny]


# @permission_classes([permissions.IsAuthenticated])
# class SpecificationViewSet(viewsets.ModelViewSet):
#    queryset = Specification.objects.all()
#    serializer_class = SpecificationSerializer
#    permission_classes = [permissions.AllowAny]

# @permission_classes([permissions.IsAuthenticated])
# class AvisClientProduitArtisanalViewSet(viewsets.ModelViewSet):
#    queryset = AvisClientProduitArtisanal.objects.all()
#    serializer_class = AvisClientProduitArtisanalSerializer
#    permission_classes = [permissions.AllowAny]

# @permission_classes([permissions.IsAuthenticated])
# class ImageProduitArtisanalViewSet(viewsets.ModelViewSet):
#    queryset = ImageProduitArtisanal.objects.all()
#    serializer_class = ImageProduitArtisanalSerializer
#    permission_classes = [permissions.AllowAny]

# @permission_classes([permissions.IsAuthenticated])
# class ProduitArtisanalDetailView(generics.RetrieveAPIView):
#    queryset = ProduitArtisanal.objects.all()
#    serializer_class = ProduitArtisanalDetailSerializer
#    permission_classes = [permissions.AllowAny]

# API Views


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
            {"error": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND
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


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def filter_produits(request):
    specifications = request.data.get("specifications", [])

    if not specifications:
        return Response(
            {"error": "Aucune spécification fournie"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    spec_ids = [spec["id"] for spec in specifications if "id" in spec]

    produits = ProduitArtisanal.objects.filter(
        specifications__id__in=spec_ids
    ).distinct()

    serializer = ProduitArtisanalSerializer(produits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def commandeList(request, artisanat_id=None):
    if artisanat_id is not None:
        # Filtrer les commandes par artisanat_id
        produits = ProduitArtisanal.objects.filter(artisanat__id=artisanat_id)
        queryset = Commande.objects.filter(panier__produits__in=produits)

        if not queryset.exists():
            return Response(
                {"message": "Aucune commande reçue pour vous"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CommandeSerializer(queryset, many=True)
        return Response(serializer.data)

    return Response(
        {"error": "Artisanat ID non fourni"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def commandeListDetail(request, artisanat_id=None, produit_id=None):
    if artisanat_id is not None:
        # Filtrer les produits par artisanat_id
        produits = ProduitArtisanal.objects.filter(artisanat__id=artisanat_id)

        if produit_id is not None:
            produits = produits.filter(id=produit_id)

        # Filtrer les commandes par les produits trouvés
        queryset = Commande.objects.filter(
            panier__itempanier__produit__in=produits
        ).distinct()

        if not queryset.exists():
            return Response(
                {"message": "produit introuvable"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommandeProduitSerializer(queryset, many=True)
        return Response(serializer.data)

    return Response(
        {"error": "Artisanat ID non fourni"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def clientList(request, artisanat_id):
    try:
        produits = ProduitArtisanal.objects.filter(artisanat__id=artisanat_id)

        # Obtenir les commandes associées à ces produits
        commandes = Commande.objects.filter(panier__produits__in=produits)

        # Obtenir les clients associés à ces commandes
        clients = Client.objects.filter(commandes__in=commandes).distinct()

        # Sérialiser les clients
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    except Artisanat.DoesNotExist:
        return Response(
            {"error": "Artisanat non trouvé"}, status=status.HTTP_404_NOT_FOUND
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
