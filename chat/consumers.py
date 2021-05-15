from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from authorize.models import User
from .models import Dialog, Message

import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        name = self.scope['url_route']['kwargs']['room']
        self.dialog_id = Dialog.objects.get(name=name).id
        self.name = f"{name}_{self.dialog_id}"

        self.user = User.objects.get(login=self.scope["cookies"]["login"])

        async_to_sync(self.channel_layer.group_add)(
            self.name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code: int):
        async_to_sync(self.channel_layer.group_discard)(
            self.name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        content_type = data.get("type")

        if content_type == "send_message":
            text = data.pop('message').strip()
            if len(text) < 5 or len(text) > 2048:
                return

            msg = Message.objects.create(dialog_id=self.dialog_id, at=self.user, text=text)
            async_to_sync(self.channel_layer.group_send)(
                self.name, {'type': 'send_message', **self.format_message(msg)}
            )

    def send_message(self, event):
        self.send(text_data=json.dumps(event["message"]))

    def format_message(self, msg: Message):
        return {"message": {
            'type': 'message',
            'text': msg.text,
            'user': self.user.login,
            'date': msg.date(),
            'photo': self.user.photo.url
        }}
