from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArtisanatViewSet,
    ProduitArtisanalDetailView,
    ProduitArtisanalViewSet,
    PanierViewSet,
    ItemPanierViewSet,
    CommandeViewSet,
)

# Créez un routeur et enregistrez vos viewsets
router = DefaultRouter()
router.register(r"artisanats", ArtisanatViewSet)
router.register(r"produits-artisanaux", ProduitArtisanalViewSet)
router.register(r"paniers", PanierViewSet)
router.register(r"items-panier", ItemPanierViewSet)
router.register(r"commandes", CommandeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "produit/<int:pk>/",
        ProduitArtisanalDetailView.as_view(),
        name="produit-artisanal-detail",
    ),
]
