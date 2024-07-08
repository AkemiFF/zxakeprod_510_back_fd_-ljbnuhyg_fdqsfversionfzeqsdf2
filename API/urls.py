from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from API import views
urlpatterns = [
    path('hebergement/', include('Hebergement.urls')),
    path('admin/', views.admin_endpoint, name='admin_endpoint'),
    path('info/', include('Accounts.urls')),
    path('user/', views.user_endpoint, name='user_endpoint'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
