from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from chatapp.chat.api.serializers import ChatSerializer
from chatapp.users.api.serializers import SendOTPSerializer, LoginSerializer, \
    ProfileSerializer

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


class ProfileViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                     GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    search_fields = ["username", "phone_number"]

    @extend_schema(methods=["GET"], request=LoginSerializer,
                   responses=LoginSerializer)
    @action(methods=["GET"], detail=True, url_path="user-chats", url_name="user-chats")
    def user_chats(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        response_serializer = ChatSerializer(instance=user.chat_set.all(), many=True)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
