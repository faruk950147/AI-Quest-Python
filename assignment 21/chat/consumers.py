from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("connected from frontend...")
        print("channel_name:", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=text_data)
        print("received from frontend...", text_data)
    
    async def disconnect(self, close_code):
        print("disconnected...")