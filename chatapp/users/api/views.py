from django.contrib.auth import get_user_model
from django.db import connection
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from chatapp.chat.api.serializers import ChatSerializer, MessageSerializer, \
    NewChatSerializer
from chatapp.chat.models import Chat
from chatapp.users.api.serializers import SendOTPSerializer, LoginSerializer, \
    ProfileSerializer
from chatapp.utils.serializers import UserIDSerializer

User = get_user_model()


class AuthViewSet(ViewSet):
    permission_classes = []

    @extend_schema(methods=["POST"], request=SendOTPSerializer,
                   responses=SendOTPSerializer)
    @action(methods=["post"], detail=False, url_path="send-otp", url_name="send-otp")
    def sent_otp(self, request):
        data_serializer = SendOTPSerializer(data=request.data)
        if data_serializer.is_valid():
            data = data_serializer.validated_data
            user, created = User.objects.get_or_create(
                phone_number=data.get("phone_number"))
            user.save()
            # send_sms(user.phone_number,user.otp_code)
            return Response(data={"data": "an otp has been sent to given phone number"},
                            status=status.HTTP_200_OK)
        return Response(data=data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(methods=["POST"], request=LoginSerializer,
                   responses=LoginSerializer)
    @action(methods=["post"], detail=False, url_path="login", url_name="login")
    def login(self, request):
        data_serializer = LoginSerializer(data=request.data)
        if data_serializer.is_valid():
            return Response(data=data_serializer.data, status=status.HTTP_200_OK)
        return Response(data=data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    search_fields = ["username", "phone_number"]

    @extend_schema(methods=["GET"], responses=ProfileSerializer)
    @action(methods=["GET"], detail=False, url_path="me", url_name="me")
    def me(self, request):
        response_serializer = ProfileSerializer(instance=request.user)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=["PUT", "PATCH"], request=ProfileSerializer,
                   responses=ProfileSerializer)
    @action(methods=["PUT", "PATCH"], detail=False, url_path="update-profile",
            url_name="update-profile")
    def update_profile(self, request):
        partial = request.method == 'PATCH'
        data_serializer = ProfileSerializer(instance=request.user,
                                            data=request.data, partial=partial)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data=data_serializer.data, status=status.HTTP_200_OK)
        return Response(data=data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(methods=["GET"], responses=ProfileSerializer)
    @action(methods=["GET"], detail=False, url_path="user-chats", url_name="user-chats")
    def user_chats(self, request):
        user = request.user
        chat_ids = tuple(user.chat_set.all().values_list("id", flat=True))
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT user_id FROM chat_chat_members 
                    WHERE chat_id IN {chat_ids} 
                    AND user_id != {request.user.id}""")
            rows = cursor.fetchall()
        user_ids = [row[0] for row in rows]
        user_chat_list = User.objects.filter(pk__in=user_ids)
        response_serializer = ProfileSerializer(instance=user_chat_list, many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(methods=["POST"], request=UserIDSerializer, responses=ChatSerializer)
    @action(methods=["POST"], detail=False, url_path="get-user-chat",
            url_name="get-user-chat")
    def get_user_chat(self, request):
        data_serializer = UserIDSerializer(data=request.data)
        if data_serializer.is_valid():
            user = get_object_or_404(User.objects.exclude(pk=request.user.pk),
                                     pk=data_serializer.validated_data.get("user"))
            chat = Chat.objects.filter(members=request.user.pk).filter(
                members=user.pk).first()
            if chat:
                response_serializer = MessageSerializer(instance=chat.message_set.all(),
                                                        many=True)
                return Response(data=response_serializer.data,
                                status=status.HTTP_200_OK)
            return Response(data={"error": "chat not found"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(data=data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(methods=["POST"], request=NewChatSerializer,
                   responses=ChatSerializer)
    @action(methods=["POST"], detail=False, url_path="new-chat",
            url_name="new-chat")
    def new_chat(self, request):
        data_serializer = NewChatSerializer(data=request.data,
                                            context={"creator_user": request.user})
        if data_serializer.is_valid():
            chat = data_serializer.save()
            response_serializer = ChatSerializer(instance=chat)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        return Response(data=data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
