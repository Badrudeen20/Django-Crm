import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'GeeksforGeeks'
        }))
    
    def disconnect(self, close_code):
        pass
    
    def receive(self, text_data):
        pass
    
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'movieplanet'

        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.disconnect(close_code)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        session = self.scope['session']
        customer = session.get('customer', 'Anonymous')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user':customer['id']
            }
        )
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        session = self.scope['session']
        customer = session.get('customer', 'Anonymous')
        if customer['id'] != user:
            content = (f'<div class="media media-chat">'
                       f'  <div class="media-body">'
                       f'     <p><span>{message}</span></p>'
                       f'  </div>'
                       f'</div>')

        else:
            content = (f'<div class="media media-chat media-chat-reverse">'
                       f'  <div class="media-body w-100">'
                       f'     <p><span>{message}</span></p>'
                       f'  </div>'
                       f'</div>')
        await self.send(text_data=json.dumps({
            'message': content,
            'user':user
        }))