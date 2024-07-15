from django.urls import path
from .import views

urlpatterns = [
    path('client-update/<int:pk>/ban/', views.update_ban_status,
         name='client-ban-update'),
    path('get_count_client/', views.get_count_client, name='get_count_client'),

    path('type-responsable/<int:pk>/', views.type_responsable_detail,
         name='type_responsable_detail'),

    path('type-responsable/create/', views.type_responsable_create,
         name='type_responsable_create'),
    path('type-responsable/update/<int:pk>/',
         views.type_responsable_update, name='type_responsable_update'),
    path('type-responsable/delete/<int:pk>/',
         views.type_responsable_delete, name='type_responsable_delete'),

    # URLs pour ResponsableEtablissement
    path('responsable-etablissement/<int:pk>/',
         views.responsable_etablissement_detail, name='responsable_etablissement_detail'),
    path('responsable-etablissement/create/', views.responsable_etablissement_create,
         name='responsable_etablissement_create'),
    path('responsable-etablissement/update/<int:pk>/',
         views.responsable_etablissement_update, name='responsable_etablissement_update'),
    path('responsable-etablissement/delete/<int:pk>/',
         views.responsable_etablissement_delete, name='responsable_etablissement_delete'),

    # URLs pour TypeCarteBancaire
    path('type-carte-bancaire/<int:pk>/', views.type_carte_bancaire_detail,
         name='type_carte_bancaire_detail'),
    path('type-carte-bancaire/create/', views.type_carte_bancaire_create,
         name='type_carte_bancaire_create'),
    path('type-carte-bancaire/update/<int:pk>/',
         views.type_carte_bancaire_update, name='type_carte_bancaire_update'),
    path('type-carte-bancaire/delete/<int:pk>/',
         views.type_carte_bancaire_delete, name='type_carte_bancaire_delete'),

    # URLs pour Client
    path('client/<int:pk>/', views.client_detail,
         name='client_detail'),  # Urls pour obtenir un Client
    # Urls pour obtenir tous les clients
    path('clients/', views.fetch_clients_detail, name='fecth_clients_detail'),
    path('client/create/', views.client_create, name='client_create'),
    path('client/create-with-username/',
         views.create_client_with_email, name='client_create'),
    path('client/create/emailinfo/',
         views.client_create_email_info, name='client_create'),
    path('client/update/<int:pk>/', views.client_update, name='client_update'),
    path('client/delete/<int:pk>/', views.client_delete, name='client_delete'),

    # Registers
    path('client/login/', views.client_login, name='client_login'),
    path('client/check-email/', views.CheckEmailView.as_view(), name='client_login'),
    path('client/loginwithemail/',
         views.client_login_with_email, name='client_login'),
    # path('registers/', views.RegisterView.as_view(), name='register'),
    path('responsables/type/<int:type_id>/',
         views.ResponsableEtablissementListByTypeView.as_view(), name='responsables-by-type'),
    path('check-admin/', views.AdminCheckAPIView.as_view(),
         name='check-admin-status'),
    path('send-verification-code/', views.send_verification_code,
         name='send_verification_code'),
    path('send-recovery-code/', views.send_recovery_code,
         name='send_recovery_code'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
