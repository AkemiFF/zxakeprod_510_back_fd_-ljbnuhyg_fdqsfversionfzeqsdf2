from django.urls import path
from Hebergement import views


urlpatterns = [
    # Nombre hebergement creer
    path('get-count-hebergement/', views.get_count, name='hebergement-count'),
    path('responsable/<int:responsable_id>/',
         views.HebergementListByResponsableView.as_view(), name='hebergements-by-responsable'),

    # HEBERGEMENT (get tout les hebergements, visualiser selon id hebergement, post, modifier, et delete Hebergement)
    path('get-all-hebergement/', views.get_all_hebergements, name='hebergement-all'),
    path('get-id-hebergement/<int:hebergement_id>/',
         views.get_hebergement_details, name='hebergement-id'),

    path('create-hebergement/', views.create_hebergement,
         name='hebergement-create'),
    path('update-hebergement/<int:hebergement_id>/',
         views.update_hebergement, name='update-hebergement'),
    path('delete-hebergements/<int:pk>/',
         views.delete_hebergement, name='delete_hebergement'),

    # Get hebergement avec son id responsable(rehefa tafa connecte de azo le id)== Responsable eteblissement
    path('get-resp-hebergement/<int:responsable_id>/',
         views.get_idresp_hebergements, name='hebergement-get-responsable'),

    # Get hebergement accessoire selon hebergement creer par responsable
    path('get-accessoire-hebergement/<int:hebergement_id>/',
         views.get_accessoires_hebergement, name='hebergement-accessoire-list'),

    # Accessoire par defaut
    path('accessoire_hebergement/<int:pk>/',
         views.get_accessoire_hebergement, name='get_accessoire_hebergement'),
    path('accessoire_hebergement/', views.create_accessoire_hebergement,
         name='create_accessoire_hebergement'),
    path('accessoire_hebergement/<int:pk>/',
         views.update_accessoire_hebergement, name='update_accessoire_hebergement'),
    path('accessoire_hebergement/<int:pk>/',
         views.delete_accessoire_hebergement, name='delete_accessoire_hebergement'),

    # Accessoire chambre par defaut
    path('accessoires-chambre/', views.get_accessoire_chambre,
         name='get_accessoire_chambre'),
    path('accessoires-chambre/create/', views.create_accessoire_chambre,
         name='create_accessoire_chambre'),
    path('accessoires-chambre/update/<int:pk>/',
         views.update_accessoire_chambre, name='update_accessoire_chambre'),
    path('accessoires-chambre/delete/<int:pk>/',
         views.delete_accessoire_chambre, name='delete_accessoire_chambre'),

    # Chambre personaliser
    path('chambre_personaliser/', views.chambre_personaliser_list,
         name='chambre_personaliser_list'),
    path('chambre_personaliser/<int:pk>/',
         views.chambre_personaliser_detail, name='chambre_personaliser_detail'),

    # Chambre par defaut admin
    path('get-post-chambres/', views.get_post_chambres, name='get-post-chambres'),
    path('put-delete-chambre/<int:pk>/',
         views.put_delete_chambre, name='put-delete-chambre'),
     path('avis-clients/', views.AvisClientsListView.as_view(), name='avis-clients-list'),
]
