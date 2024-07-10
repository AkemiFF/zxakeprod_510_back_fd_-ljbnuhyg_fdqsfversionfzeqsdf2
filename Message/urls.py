from django.urls import path
from .views import (
    MessageListCreateView,
    HebergementMessageListCreateView,
    MessageDetailView,
    HebergementMessageDetailView
)

urlpatterns = [
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('hebergement-messages/', HebergementMessageListCreateView.as_view(), name='hebergement-message-list-create'),
    path('hebergement-messages/<int:pk>/', HebergementMessageDetailView.as_view(), name='hebergement-message-detail'),
]
