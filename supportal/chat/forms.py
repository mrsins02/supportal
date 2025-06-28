from django import forms
from django.core.exceptions import ValidationError

from supportal.chat.models import Chat


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = [
            "members",
        ]

    def clean(self):
        cleaned_data = super().clean()
        members = cleaned_data.get("members")
        print(members)
        if len(members) != 2:
            raise ValidationError({"members": "A chat must have exactly 2 members"})
        member1, member2 = members[0], members[1]
        existing_chats = Chat.objects.filter(members=member1).filter(members=member2)
        if existing_chats.exists():
            raise ValidationError(
                {"members": "A chat between these two users already exists"}
            )
