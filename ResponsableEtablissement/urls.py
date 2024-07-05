# ResponsableEtablissement/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_responsables_etablissement, name='responsables-list'),
    path('get/<int:pk>', views.get_responsable_etablissement_detail,
         name='responsable-detail'),
    path('signup', views.signup_responsable, name='signup_responsable'),
    path('update/<int:pk>', views.update_responsable_etablissement,
         name='responsable-update'),
    path('delete/<int:pk>', views.delete_responsable_etablissement,
         name='responsable-delete'),
    path('login', views.responsable_etablissement_login,
         name='responsable_etablissement_login'),

]
