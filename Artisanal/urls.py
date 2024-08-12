from django.urls import path
from .views import (
    ProduitArtisanalViewSet,
    PanierViewSet,
    ItemPanierViewSet,
    add_to_cart,
    check_if_client_liked_product,
    like_produit,
    filter_produits,
    LocalisationArtisanatViewSet,
    ResponsableEtablissementViewSet,
    commandeList,
    clientList,
    artisanantList,
    commandeListDetail
)



urlpatterns = [
    # Routes pour les produits artisanaux
    path('<int:artisanat_id>/produits/', ProduitArtisanalViewSet.as_view({'get': 'list'}), name='list-produit-artisanal-par-artisanat'),
    path('<int:artisanat_id>/produits/<int:pk>/', ProduitArtisanalViewSet.as_view({'get': 'retrieve'}), name='detail-produit-artisanal-par-artisanat'),

    # Routes pour les commandes
    path('<int:artisanat_id>/commandes/', commandeList, name='commande-list'),
    path('<int:artisanat_id>/commandes/<int:produit_id>/',commandeListDetail, name='detail-commande'),

    # Routes pour les clients
    path('<int:artisanat_id>/clients/', clientList, name='client-list'),
    path('<int:artisanat_id>/clients/<int:pk>/', clientList, name='detail-client'),

    # Routes pour l'artisanat
    path('<int:artisanat_id>/', artisanantList, name='list-artisanat'),
    path('<int:artisanat_id>/<int:pk>/', artisanantList, name='detail-artisanat'),

    # Routes pour la gestion du panier
    path('panier/ajouter/', add_to_cart, name='add-to-cart'),
    path('panier/', PanierViewSet.as_view({'get': 'list'}), name='list-panier'),
    path('panier/items/', ItemPanierViewSet.as_view({'get': 'list'}), name='list-item-panier'),

    # Routes pour la localisation et le responsable d'établissement
    path('<int:artisanat_id>/localisations/', LocalisationArtisanatViewSet, name='list-localisation-artisanat'),
    path('<int:artisanat_id>/responsables/', ResponsableEtablissementViewSet, name='list-responsable-etablissement'),

    # API pour les interactions avec les produits
    path('produits/<int:produit_id>/liked/', check_if_client_liked_product, name='check_if_client_liked_product'),
    path('produits/like/', like_produit, name='like_produit'),
    path('produits/filter/', filter_produits, name='filter_produits'),
]
