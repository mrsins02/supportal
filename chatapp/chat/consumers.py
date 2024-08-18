import base64
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.files.base import ContentFile

from .models import Message, Chat


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_name = f"chat_{self.chat_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name
        )

        self.accept()

        # validate chat
        chat = Chat.objects.filter(pk=self.chat_id)
        if not chat.exists():
            self.send(text_data=json.dumps({"error": "chat not found"}))
            self.close(code=1011)
        chat = chat.first()

        # validate user
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.send(text_data=json.dumps({"error": self.scope["error"]}))
            self.close(code=3000)

        # validate user to be member of the chat
        if self.user not in chat.members.all():
            self.send(
                text_data=json.dumps({"error": "you are not a member of this chat"}))
            self.close(code=3003)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # validate empty message
        if len(data.get("message", "")) < 1:
            self.send(text_data=json.dumps({"error": "message is empty"}))
            self.close(code=1011)

        new_message = Message.objects.create(
            chat_id=self.chat_id,
            message=data.get("message"),
            author_id=self.user.pk,
        )
        attachment = data.get("attachment")
        if attachment:
            # convert file from base64 and save to field
            file_name, file_content = self.proccess_file(attachment, self.chat_name)
            new_message.attachment = ContentFile(file_content, name=file_name)
        new_message.save()

        send_data = json.dumps({
            "id": new_message.pk,
            "created_at": new_message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "author": new_message.author_id,
            "message": new_message.message,
            "attachment": new_message.attachment.url
        })

        # send the message to chat
        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            {
                "type": "chat_message",
                "data": send_data
            }
        )

    def proccess_file(self, file, name):
        """
        convert base64 encoded file to file
        """
        format, file_str = file.split(';base64,')
        ext = format.split('/')[-1]
        return f"{name}.{ext}", base64.b64decode(file_str)

    def chat_message(self, event):
        message = event["data"]
        self.send(text_data=message)
