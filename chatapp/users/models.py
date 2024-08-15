from django.contrib.auth.models import AbstractUser
from django.db import models

from chatapp.utils.models import upload_location, generate_random_number


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=11,
        unique=True,
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
        default='media/no_avatar.jpg',
    )
    otp_code = models.CharField(
        max_length=4,
        blank=True,
        default=generate_random_number,
        verbose_name="OTP Code"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['first_name', 'last_name', "username", "phone_number"]

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.username = self.phone_number
        return super().save(*args, **kwargs)
