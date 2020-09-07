import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *


class SocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close(1234)
        self.room = self.scope['user'].user_id
        print(self.scope['user'])
        await self.channel_layer.group_add(
            self.room,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room,
            self.channel_name
        )
        self.close(0)

    @database_sync_to_async
    def get_name(self):
        return User.objects.get(username=self.room_name)

    @database_sync_to_async
    def store_message(self, data):

        sender = UserDetails(user=User(user_id=data['sender_id']))
        recipient = UserDetails(user=User(user_id=data['recipient_id']))
        print(sender)
        print(recipient)
        try:
            conversion = Conversation.objects.get(sender=sender, recipient=recipient)
            conversion.unseen_message += 1
            conversion.save()
        except Conversation.DoesNotExist as e:
            conversion = Conversation(
                sender=sender,
                recipient=recipient,
                last_message=data['message'],

            )
            conversion.save()
        try:
            conversion = Conversation.objects.get(sender=recipient, recipient=sender)
            conversion.unseen_message += 1
            conversion.last_message = data['message']
            conversion.save()
        except Conversation.DoesNotExist as e:
            conversation = Conversation(
                sender=recipient,
                recipient=sender,
                last_message=data['message'],
                unseen_message=1
            )
            conversation.save()

        message = Messages(message_id=data['message_id'],
                           conversation_id=data['conversation_id'],
                           sender_id=data['sender_id'],
                           recipient_id=data['recipient_id'],
                           message=data['message'],
                           message_type=data['message_type'],
                           )
        message.save()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('text_data_json', text_data_json)
        if text_data_json['type'] == 'message':
            #try:
            await self.store_message(message)
            #except Exception as e:
            #    print('error', e)
            #    pass

            await self.channel_layer.group_send(
                message['recipient_id'],
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))
