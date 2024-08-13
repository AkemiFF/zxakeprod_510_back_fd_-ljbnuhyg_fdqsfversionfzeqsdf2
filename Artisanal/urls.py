from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

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
    path(
        "produits/<int:produit_id>/liked/",
        check_if_client_liked_product,
        name="check_if_client_liked_product",
    ),
    path("panier/ajouter/", add_to_cart, name="add-to-cart"),
    path("produit/<int:produit_id>/like/", like_produit, name="like_produit"),
    path("produits/filter/", filter_produits, name="filter_produits"),
    path("client-panier/", PanierView.as_view(), name="panier-client"),
]
