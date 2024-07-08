from django.urls import path
from .import views

urlpatterns = [

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
    path('client/<int:pk>/', views.client_detail, name='client_detail'),
    path('client/create/', views.client_create, name='client_create'),
#     path('client/login/', views.login_view, name='client_login'),
    path('client/update/<int:pk>/', views.client_update, name='client_update'),
    path('client/delete/<int:pk>/', views.client_delete, name='client_delete'),

     # Registers
     # path('registers/', views.RegisterView.as_view(), name='register'),

]
