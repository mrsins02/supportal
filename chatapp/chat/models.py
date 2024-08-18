from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

from chatapp.utils.models import upload_location

User = get_user_model()


class Chat(models.Model):
    members = models.ManyToManyField(
        to=User,
        verbose_name="Members"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}"


class Message(models.Model):
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        verbose_name="Chat"
    )
    message = models.TextField(
        verbose_name="Message"
    )
    attachment = models.FileField(
        upload_to=upload_location,
        blank=True,
        null=True,
        verbose_name="Attachment",
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Author"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.phone_number}({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"

    def clean(self):
        if self.author_id not in self.chat.members.all().values_list('id',
                                                                     flat=True):
            raise ValidationError(
                {"author": "author must be one of the chat members"})
