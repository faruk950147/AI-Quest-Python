from channels.consumer import SyncConsumer, AsyncConsumer
import time
import asyncio
'''
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
        

#  real time data streaming
class OfficeSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })
    
    def websocket_receive(self, event):
        print(f'WebSocket received: {event["text"]}')
        for i in range(50):
            self.send({
                'type': 'websocket.send',
                'text': f'Message {i+1}'
            })
            time.sleep(1)
    
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
        print(f'WebSocket received: {event["text"]}')
        for i in range(5):
            await self.send({
                'type': 'websocket.send',
                'text': f'Message {i+1}'
            })
            await asyncio.sleep(1)
    
    async def websocket_disconnect(self, event):
        await self.send({
            'type': 'websocket.close'
        })
'''        
 
class OfficeSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })
    
    def websocket_receive(self, event):
        print(f'WebSocket received: {event["text"]}')
        for i in range(50):
            self.send({
                'type': 'websocket.send',
                'text': f'Message {i+1}'
            })
            time.sleep(1)
    
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
        print(f'WebSocket received: {event["text"]}')
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
    
    async def websocket_disconnect(self, event):
        self.send({
            'type': 'websocket.close'
        })
        
        