from django.urls import path
from .views import *

urlpatterns = [
    # path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('get-client-hebergement/', get_messages_client_hebergement, name='message-list-h-c'),
    # path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    # path('hebergement-messages/', HebergementMessageListCreateView.as_view(), name='hebergement-message-list-create'),
    # path('hebergement-messages/<int:pk>/', HebergementMessageDetailView.as_view(), name='hebergement-message-detail'),
]
