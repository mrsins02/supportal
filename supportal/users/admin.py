from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "is_active")
    list_display_links = (
        "id",
        "phone_number",
    )
    list_filter = ("is_active", "is_superuser", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("id",)
    fieldsets = (
        (None, {"fields": ("username", "password", "otp_code")}),
        (
            "Personal info",
            {"fields": ("avatar", "first_name", "last_name", "phone_number", "email")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
