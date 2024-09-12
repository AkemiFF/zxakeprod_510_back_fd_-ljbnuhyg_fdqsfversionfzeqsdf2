from django.urls import path
from Hebergement import views


urlpatterns = [
    # Reservation #
    # data format
    # {
    #     "chambre_ids": [1, 2, 3],
    #     "check_in": "2024-08-20",
    #     "check_out": "2024-08-25"
    # }
    path(
        "client/reservations/",
        views.ClientReservationsListView.as_view(),
        name="client-reservations",
    ),
    path(
        "transactions/create/",
        views.CreateReservationView.as_view(),
        name="create-transaction",
    ),
    path(
        "check/",
        views.check_availability_and_calculate_price,
        name="check_availability",
    ),
    #########################################
    # For Super Admin #
    path("list/", views.AdminHebergementListView.as_view(), name="hebergement-list"),
    path(
        "deleted/", views.DeletedHebergementListView.as_view(), name="hebergement-list"
    ),
    path(
        "type/",
        views.TypeHebergementListView.as_view(),
        name="type-hebergement",
    ),
    path(
        "toggle-autorisation/<int:pk>/",
        views.ToggleAutorisationView.as_view(),
        name="toggle_autorisation",
    ),
    path(
        "toggle-delete/<int:pk>/",
        views.ToggleDeleteHebergement.as_view(),
        name="toggle_delete",
    ),
    #########################################
    path(
        "localisation/create/",
        views.CreateLocalisationView.as_view(),
        name="create-localisation",
    ),
    path(
        "<int:hebergement_id>/stats/",
        views.HebergementStatsView.as_view(),
        name="hebergement-stats",
    ),
    path(
        "<int:hebergement_id>/reservations/mois/",
        views.ReservationCountByMonthView.as_view(),
        name="reservation-stats",
    ),
    path(
        "client-reservations/<int:client_id>/hebergement/<int:hebergement_id>/",
        views.ClientReservationsView.as_view(),
        name="client_reservations",
    ),
    path(
        "reservations-by-day/<int:hebergement_id>/",
        views.ReservationsByDayOfWeekView.as_view(),
        name="reservations_by_day_of_week",
    ),
    path(
        "<int:hebergement_id>/recent-reservations/",
        views.RecentReservationsForHebergementView.as_view(),
        name="recent_reservations_for_hebergement",
    ),
    path(
        "add-hebergement-image/",
        views.AddHebergementImageView.as_view(),
        name="add-hebergement-image",
    ),
    path(
        "reservations/<int:hebergement_id>/",
        views.ReservationsByHebergementView.as_view(),
        name="reservations-by-hebergement",
    ),
    path(
        "clients-et-chambres/<int:hebergement_id>/",
        views.ClientsAndChambresByHebergementView.as_view(),
        name="clients-and-chambres-by-hebergement",
    ),
    path(
        "info/<int:hebergement_id>/",
        views.MinHebergementDetailView.as_view(),
        name="hebergement-detail",
    ),
    #########################""
    path(
        "type-hebergement/",
        views.TypeHebergementListView.as_view(),
        name="type-hebergement-list",
    ),
    path("get-count-hebergement/", views.get_count, name="hebergement-count"),
    path(
        "responsable/<int:responsable_id>/",
        views.HebergementListByResponsableView.as_view(),
        name="hebergements-by-responsable",
    ),
    # HEBERGEMENT (get tout les hebergements, visualiser selon id hebergement, post, modifier, et delete Hebergement)
    path(
        "get-image-location/<str:location>/",
        views.get_accommodations_by_city_or_address,
        name="get_accommodations_by_city",
    ),
    path("cities/", views.get_unique_cities, name="get_unique_cities"),
    path("get-all-hebergement/", views.get_all_hebergements, name="hebergement-all"),
    path(
        "suggestion/", views.get_suggestion_hebergements, name="hebergement-suggesion"
    ),
    path("get-all-amenities/", views.get_all_accessoire, name="get-all-accessoire"),
    path(
        "get-id-hebergement/<int:hebergement_id>/",
        views.get_hebergement_details,
        name="hebergement-id",
    ),
    path(
        "<int:hebergement_id>/reservations/",
        views.HebergementReservationsListView.as_view(),
        name="hebergement-reservations",
    ),
    path(
        "get-id-chambre/<int:chambre_id>/",
        views.get_chambre_details,
        name="chambre-id",
    ),
    path(
        "create-hebergement/", views.create_new_hebergement, name="hebergement-create"
    ),
    path(
        "update-hebergement/<int:hebergement_id>/",
        views.update_hebergement,
        name="update-hebergement",
    ),
    path(
        "delete-hebergements/<int:pk>/",
        views.delete_hebergement,
        name="delete_hebergement",
    ),
    # Get hebergement avec son id responsable(rehefa tafa connecte de azo le id)== Responsable eteblissement
    path(
        "get-resp-hebergement/<int:responsable_id>/",
        views.get_idresp_hebergements,
        name="hebergement-get-responsable",
    ),
    # Get hebergement accessoire selon hebergement creer par responsable
    path(
        "get-accessoire-hebergement/<int:hebergement_id>/",
        views.get_accessoires_hebergement,
        name="hebergement-accessoire-list",
    ),
    # Accessoire par defaut
    path(
        "accessoire_hebergement/<int:pk>/",
        views.get_accessoire_hebergement,
        name="get_accessoire_hebergement",
    ),
    path(
        "accessoire_hebergement/",
        views.create_accessoire_hebergement,
        name="create_accessoire_hebergement",
    ),
    path(
        "accessoire_hebergement/<int:pk>/",
        views.update_accessoire_hebergement,
        name="update_accessoire_hebergement",
    ),
    path(
        "accessoire_hebergement/<int:pk>/",
        views.delete_accessoire_hebergement,
        name="delete_accessoire_hebergement",
    ),
    # Accessoire chambre par defaut
    path(
        "accessoires-chambre/",
        views.get_accessoire_chambre,
        name="get_accessoire_chambre",
    ),
    path(
        "accessoires-chambre/create/",
        views.create_accessoire_chambre,
        name="create_accessoire_chambre",
    ),
    path(
        "accessoires-chambre/update/<int:pk>/",
        views.update_accessoire_chambre,
        name="update_accessoire_chambre",
    ),
    path(
        "accessoires-chambre/delete/<int:pk>/",
        views.delete_accessoire_chambre,
        name="delete_accessoire_chambre",
    ),
    # Chambre personaliser
    path(
        "chambre_personaliser/",
        views.chambre_personaliser_list,
        name="chambre_personaliser_list",
    ),
    path(
        "chambre_personaliser/<int:pk>/",
        views.chambre_personaliser_detail,
        name="chambre_personaliser_detail",
    ),
    # Chambre par defaut admin
    path("get-post-chambres/", views.get_post_chambres, name="get-post-chambres"),
    path(
        "put-delete-chambre/<int:pk>/",
        views.put_delete_chambre,
        name="put-delete-chambre",
    ),
    path(
        "avis-clients/", views.AvisClientsListView.as_view(), name="avis-clients-list"
    ),
    path(
        "generer-description/<int:hebergement_id>/",
        views.generer_description_view,
        name="generer_description",
    ),
    path(
        "<int:hebergement_id>/like/",
        views.like_hebergement,
        name="like_hebergement",
    ),
    path(
        "<int:hebergement_id>/liked/",
        views.check_if_client_liked_hebergement,
        name="check_if_client_liked_hebergement",
    ),
    path(
        "<int:hebergement_id>/chambres/",
        views.list_chambres_by_hotel,
        name="list_chambres_by_hotel",
    ),
    path(
        "<int:pk>/commission/",
        views.edit_commission,
        name="edit_commission",
    ),
    path(
        "add-hebergement-chambre/",
        views.add_hebergement_chambre,
        name="add-hebergement-chambre",
    ),
    path(
        "edit-hebergement-chambre/<int:pk>/",
        views.edit_hebergement_chambre,
        name="edit-hebergement-chambre",
    ),
    path(
        "get-hebergement-chambre/<int:pk>/",
        views.get_hebergement_chambre,
        name="get-hebergement-chambre",
    ),
    path(
        "delete-hebergement-chambre/<int:id>/",
        views.delete_hebergement_chambre,
        name="delete-hebergement-chambre",
    ),
    path("type-chambres/", views.ChambreListView.as_view(), name="chambre-list"),
    path(
        "reservations/create/",
        views.CreateReservationView.as_view(),
        name="create-reservation",
    ),
]
