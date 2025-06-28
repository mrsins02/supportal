from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from supportal.chat.filters import MessageSearchFilter
from supportal.chat.models import Chat, Message
from supportal.utils.serializers import UserIDSerializer

User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            'id',
            'created_at',
            'members',
        )


class NewChatSerializer(UserIDSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        first_user = self.context['creator_user']
        second_user = self.context['user']
        if first_user == second_user:
            raise ValidationError({"user": 'you can not start chat with yourself'})
        return attrs

    def save(self, **kwargs):
        first_user = self.context['creator_user']
        second_user = self.context['user']
        existing_chats = Chat.objects.filter(members=first_user).filter(
            members=second_user)
        if existing_chats.exists():
            return existing_chats.first()
        new_chat = Chat()
        new_chat.save()
        new_chat.members.add(first_user)
        new_chat.members.add(second_user)
        return new_chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'chat',
            'created_at',
            'author',
            'message',
            'attachment',
        )


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    def get_messages(self, obj):
        messages = MessageSearchFilter.filter_queryset(
            request=self.context.get('request'),
            queryset=obj.message_set.all()
        )
        # messages = obj.message_set.all()
        return MessageSerializer(instance=messages, many=True).data

    class Meta:
        model = Chat
        fields = (
            'id',
            'created_at',
            'members',
            'messages',
        )
