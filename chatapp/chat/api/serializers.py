from django.contrib.auth import get_user_model
from rest_framework import serializers

from chatapp.chat.models import Chat

User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            'id',
            'created_at',
            'members',
        )
