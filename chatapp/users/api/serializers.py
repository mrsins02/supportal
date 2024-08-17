from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import RefreshToken
from chatapp.utils.validators import PhoneNumberValidator

User = get_user_model()


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        validators=[
            PhoneNumberValidator
        ],
    )


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        validators=[
            PhoneNumberValidator
        ]
    )
    otp_code = serializers.CharField(
        max_length=5
    )

    def validate(self, attrs):
        user = User.objects.filter(phone_number=attrs.get('phone_number'))
        if not user.exists():
            error = "user with given phone number does not exist"
            raise ValidationError({"phone_number": error})
        user = user.first()
        if not user.otp_code == attrs.get("otp_code"):
            error = "otp code does not match"
            raise ValidationError(error)
        self.context['user'] = user
        return attrs

    def to_representation(self, instance):
        user = self.context["user"]
        refresh = RefreshToken.for_user(user)
        # user.otp_code = GenerateRandomCode(length=5)()
        # user.save()
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
