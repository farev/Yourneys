import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils.timesince import timesince

from chat.models import ConversationMessage
from chat.serializers import ConversationMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        #Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        #Leave room
        print("disconecting")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        #Receive message form WebSocket
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        #created_at = text_data_json['created_at']
        #message = ConversationMessage.objects.get(pk=text_data_json['messageID']) 

        #print("Receive: ", type)

        if type == 'message':
            print('message')
            #Send message to group
            await self.channel_layer.group_send(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                })
            
    async def chat_message(self, event):
        #print('message')
        #Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
        }))
