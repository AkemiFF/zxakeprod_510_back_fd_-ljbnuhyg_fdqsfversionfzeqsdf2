from django.urls import path
from Hebergement import views



urlpatterns = [
    # Nombre hebergement creer
    path('get-count-hebergement/', views.get_count, name='hebergement-count'),
    
    # HEBERGEMENT (get tout les hebergements, visualiser selon id hebergement, post, modifier, et delete Hebergement)
    path('get-all-hebergement/', views.get_all_hebergements, name='hebergement-all'),
    path('get-id-hebergement/<int:hebergement_id>/', views.get_id_hebergements, name='hebergement-id'),
    
    path('create-hebergement/', views.create_hebergement, name='hebergement-create'),
    path('update-hebergement/<int:hebergement_id>/', views.update_hebergement, name='update-hebergement'),
    path('delete-hebergements/<int:pk>/', views.delete_hebergement, name='delete_hebergement'),

    # Get hebergement avec son id responsable(rehefa tafa connecte de azo le id)== Responsable eteblissement
    path('get-resp-hebergement/<int:responsable_id>/', views.get_idresp_hebergements, name='hebergement-get-responsable'),
    
    # Get hebergement accessoire selon hebergement creer par responsable
    path('get-accessoire-hebergement/<int:hebergement_id>/', views.get_accessoires_hebergement, name='hebergement-accessoire-list'),

]
