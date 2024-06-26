# chat/urls.py
from django.urls import path

from .views import chat_index, room

urlpatterns = [
    path("", chat_index, name="index"),
    path("<str:room_name>/", room, name="room"),
]