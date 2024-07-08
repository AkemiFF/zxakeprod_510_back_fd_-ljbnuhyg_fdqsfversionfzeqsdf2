from django.urls import path
from Hebergement import views



urlpatterns = [
    path('get-count-hebergement/', views.get_count, name='hebergement-count'),
    path('get-all-hebergement/', views.get_all_hebergements, name='hebergement-all'),
    path('create-hebergement/', views.create_hebergement, name='hebergement-create'),
    path('update-hebergement/<int:pk>/', views.update_hebergement, name='update_hebergement'),
    path('delete-hebergements/<int:pk>/', views.delete_hebergement, name='delete_hebergement'),

    # Accessoire selectionner hebergement
    path('hebergement-accessoire_all/', views.get_hebergement_accessoires_all, name='hebergement-accessoire-list'),
    path('hebergement-accessoire/<int:hebergement_id>', views.get_hebergement_accessoires, name='hebergement-accessoire-list'),

    # Accesoire hebergement par defaut
    path('accessoire-hebergement/', views.accessoire_hebergement_list, name='accessoire-hebergement-list'),
    path('accessoire-hebergement/<int:pk>/', views.accessoire_hebergement_detail, name='accessoire-hebergement-detail'),
    path('hebergement-chambre/', views.hebergement_chambre_list, name='hebergement-chambre-list'),

    path('hebergement-accessoire/', views.hebergement_accessoire_list, name='hebergement-accessoire-list'),
    path('hebergement-accessoire/create/', views.hebergement_accessoire_create, name='hebergement-accessoire-create'),
    path('hebergement-accessoire/<int:pk>/', views.hebergement_accessoire_detail, name='hebergement-accessoire-detail'),

    # Chambre hebergement choisit
    path('hebergement-chambre/<int:hebergement_id>/', views.hebergement_chambre_list, name='hebergement-chambre-list'),
    path('hebergement-chambre/<int:hebergement_id>/<int:chambre_id>/', views.hebergement_chambre_detail, name='hebergement-chambre-detail'),

    # Chambre personnaliser 
    path('accessoire-chambre/', views.accessoire_chambre_list, name='accessoire-chambre-list'),
    path('accessoire-chambre/create/', views.accessoire_chambre_create, name='accessoire-chambre-create'),
    path('accessoire-chambre/<int:pk>/', views.accessoire_chambre_detail, name='accessoire-chambre-detail'),

    # Chambre
    path('chambre/', views.chambre_list, name='chambre-list'),
    path('api/chambre/create/', views.chambre_create, name='chambre-create'),
    path('api/chambre/<int:pk>/', views.chambre_detail, name='chambre-detail'),

    path('hebergement-chambre-accessoire/', views.hebergement_chambre_accessoire_list, name='hebergement-chambre-accessoire-list'),
    path('hebergement-chambre-accessoire/create/', views.hebergement_chambre_accessoire_create, name='hebergement-chambre-accessoire-create'),
    path('hebergement-chambre-accessoire/<int:pk>/', views.hebergement_chambre_accessoire_detail, name='hebergement-chambre-accessoire-detail'),
]
