import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("UUID"),
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("username",)

    def __str__(self) -> str:
        return self.username
