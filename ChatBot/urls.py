from django.urls import path

from ChatBot.utils import test_database
from .views import *

urlpatterns = [
    path("", chatbot, name="chatbot"),
    path("test/", test_database, name="test_chatbot"),
    path("test2/", test_chatbot_2, name="test_chatbot"),
]
