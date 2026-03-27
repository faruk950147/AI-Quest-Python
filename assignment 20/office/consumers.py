from channels.consumer import SyncConsumer, AsyncConsumer

class OfficeSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })
        print(f'WebSocket connected{self.scope["path"]}')
    
    def websocket_receive(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
        for i in range(5):
            print(f'WebSocket received: {event["text"]}')
    
    def websocket_disconnect(self, event):
        self.send({
            'type': 'websocket.close'
        })
        print(f'WebSocket disconnected  {self.scope["path"]}')

class OfficeAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })
        print(f'WebSocket connected{self.scope["path"]}')
    
    async def websocket_receive(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
        for i in range(5):
            print(f'WebSocket received: {event["text"]}')
    
    async def websocket_disconnect(self, event):
        await self.send({
            'type': 'websocket.close'
        })
        print(f'WebSocket disconnected  {self.scope["path"]}')