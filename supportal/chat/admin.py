from django.contrib import admin
from django.contrib.auth import get_user_model

from supportal.chat.forms import ChatForm
from supportal.chat.models import Chat, Message


User = get_user_model()


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )
    list_display_links = (
        "id",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "id",
        "members__id",
        "members__username",
        "members__phone_number",
    )
    readonly_fields = (
        "id",
        "created_at",
    )
    autocomplete_fields = ("members",)
    form = ChatForm
    fieldsets = ((None, {"fields": ("id", "created_at", "members")}),)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chat",
        "author",
        "created_at",
    )
    list_display_links = (
        "id",
        "chat",
    )
    list_filter = ("created_at",)
    search_fields = (
        "message",
        "author__username",
        "author__phone_number",
    )
    readonly_fields = (
        "id",
        "created_at",
    )
    autocomplete_fields = ("chat", "author")
    fieldsets = (
        (None, {"fields": ("id", "chat", "author", "created_at")}),
        (
            "Attachments",
            {
                "fields": (
                    "message",
                    "attachment",
                )
            },
        ),
    )
