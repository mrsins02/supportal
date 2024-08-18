from django.urls import path

from chatapp.chat import consumers

url_patterns = [
    path("ws/chat/<chat_id>/", consumers.ChatConsumer.as_asgi()),
]
