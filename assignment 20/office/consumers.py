from channels.consumer import SyncConsumer, AsyncConsumer

class OfficeSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })
    
    def websocket_receive(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
    
    def websocket_disconnect(self, event):
        self.send({
            'type': 'websocket.close'
        })

class OfficeAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
    
    async def websocket_disconnect(self, event):
        await self.send({
            'type': 'websocket.close'
        })