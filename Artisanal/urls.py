# urls.py
from django.urls import path
from Artisanal.views import *

urlpatterns = [
    path('artisanats/count/', get_count_artisanat, name='artisanat-count'),
    path('artisanats/all/', get_all_artisanat, name='artisanat-all'),
    path('artisanats/<int:pk>/', get_artisanat_by_id, name='artisanat-by-id'),
    path('artisanats/responsable/<int:responsable_id>/',
         get_artisanat_by_responsable_id, name='artisanat-by-responsable'),
    path('artisanats/', artisanat_list_create, name='artisanat-list-create'),
    path('artisanats/<int:pk>/', artisanat_detail, name='artisanat-detail'),


    path('artisanats/responsable/<int:responsable_id>/',
         ArtisanatListByResponsableView.as_view(), name='artisanats-by-responsable'),
    path('produits-artisanaux/artisanat/<int:artisanat_id>/',
         ProduitArtisanalListByArtisanatView.as_view(), name='produits-artisanaux-by-artisanat'),

    path('produits-artisanal/count/', get_count_produit_artisanal,
         name='produit-artisanal-count'),
    path('produits-artisanal/all/', get_all_produit_artisanal,
         name='produit-artisanal-all'),
    path('produits-artisanal/<int:pk>/', get_produit_artisanal_by_id,
         name='produit-artisanal-by-id'),
    path('produits-artisanal/responsable/<int:responsable_id>/',
         get_produit_artisanal_by_responsable_id, name='produit-artisanal-by-responsable'),
    path('produits-artisanal/', produit_artisanal_list_create,
         name='produit-artisanal-list-create'),
    path('produits-artisanal/<int:pk>/', produit_artisanal_detail,
         name='produit-artisanal-detail'),

    path('paniers/count/', get_count_panier, name='panier-count'),
    path('paniers/all/', get_all_panier, name='panier-all'),
    path('paniers/<int:pk>/', get_panier_by_id, name='panier-by-id'),
    path('paniers/', panier_list_create, name='panier-list-create'),
    path('paniers/<int:pk>/', panier_detail, name='panier-detail'),

    path('items_panier/count/', get_count_item_panier, name='item-panier-count'),
    path('items_panier/all/', get_all_item_panier, name='item-panier-all'),
    path('items_panier/<int:pk>/', get_item_panier_by_id, name='item-panier-by-id'),
    path('items_panier/', item_panier_list_create,
         name='item-panier-list-create'),
    path('items_panier/<int:pk>/', item_panier_detail, name='item-panier-detail'),

    path('commandes/count/', get_count_commande, name='commande-count'),
    path('commandes/all/', get_all_commande, name='commande-all'),
    path('commandes/<int:pk>/', get_commande_by_id, name='commande-by-id'),
    path('commandes/', commande_list_create, name='commande-list-create'),
    path('commandes/<int:pk>/', commande_detail, name='commande-detail'),
]
