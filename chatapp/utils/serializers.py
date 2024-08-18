from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserIDSerializer(serializers.Serializer):
    """
    Serializer for views need user_id and validate it
    """
    user = serializers.IntegerField()

    def validate_user(self, user):
        user = User.objects.filter(pk=user, is_active=True)
        if not user.exists():
            raise ValidationError("user does not exist")
        user = user.first()
        self.context['user'] = user
        return user.pk
