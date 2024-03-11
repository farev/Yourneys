import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils.timesince import timesince


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Conecting")
        self.group_name = 'notifications'
        #self.room_group_name = f'notifications_{self.room_name}'
        #Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        #Leave room
        print("disconecting")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        #Receive message form WebSocket
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']

        if type == 'notification':
            print('notification')
            #Send message to group
            await self.channel_layer.group_send(
                self.group_name, {
                    'type': 'send_notification',
                    'message': message,
                })
            
    async def send_notification(self, event):
        #Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
        }))

    pass