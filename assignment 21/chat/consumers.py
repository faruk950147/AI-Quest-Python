import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # Get room name from the URL route (e.g., /ws/chat/<room_name>/)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        
        print('scope:', type(self.scope))

        # Add this channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept WebSocket connection
        await self.send({
            "type": "websocket.accept"
        })
        print('WebSocket connected')
        print('channel name:', self.channel_name)
        print('room name:', self.room_name)
        print('room group name:', self.room_group_name)
        print('scope:', type(self.scope))
    
    async def websocket_receive(self, event):
        # Receive message from WebSocket
        message = event.get("text", None)
        if message:
            try:
                data = json.loads(message)  # Expecting JSON {"username": ..., "message": ...}
                username = data.get("username", "Anonymous")
                text = data.get("message", "")

                # Broadcast the message to the group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat.message",
                        "username": username,
                        "message": text,
                    }
                )
            except Exception as e:
                print("Error processing message:", e)

    async def chat_message(self, event):
        # Handler for messages sent to the group
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "username": event["username"],
                "message": event["message"],
            })
        })

    async def websocket_disconnect(self, event):
        # Remove this channel from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name} from room {self.room_name}")