from django.contrib.auth.models import AbstractUser
from django.db import models

from chatapp.utils.models import upload_location, GenerateRandomCode
from chatapp.utils.validators import PhoneNumberValidator

user_otp_generator = GenerateRandomCode(length=5)


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        validators=[
            PhoneNumberValidator
        ],
        verbose_name="Phone Number"
    )
    first_name = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="First Name"
    )
    last_name = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="Last Name"
    )
    avatar = models.ImageField(
        upload_to=upload_location,
        blank=True,
        default='no_avatar.jpg',
    )
    otp_code = models.CharField(
        max_length=5,
        blank=True,
        # default=user_otp_generator,
        default="12345",
        verbose_name="OTP Code"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['first_name', 'last_name']

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.username:
                self.username = self.phone_number
        return super().save(*args, **kwargs)
