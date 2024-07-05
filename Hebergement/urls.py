from django.urls import path
from Hebergement import views



urlpatterns = [
    path('get-count-hebergement/', views.get_count, name='hebergement-count'),
    path('get-all-hebergement/', views.get_all_hebergements, name='hebergement-all'),
    path('create-hebergement/', views.get_all_hebergements, name='hebergement-create'),
]
