from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from chatapp.users.api.serializers import SendOTPSerializer

User = get_user_model()


class ChatViewSet(ViewSet):
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
