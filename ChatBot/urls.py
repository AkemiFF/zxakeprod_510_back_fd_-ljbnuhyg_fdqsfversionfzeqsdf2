from django.urls import path
from .views import *

urlpatterns = [
    path("", chatbot, name="chatbot"),
    path("test/", test_chatbot, name="test_chatbot"),
]
