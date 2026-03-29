from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncConsumer):
    # WebSocket connection handler
    async def websocket_connect(self, event):
        # Get room name from the URL route (e.g., /ws/chat/<room_name>/)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Create group name for this room
        self.room_group_name = f"chat_{self.room_name}"
        # Add this channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accept the connection
        await self.send({
            "type": "websocket.accept"
        })
        # Print connection status
        print("Connected:", self.channel_name)


    # WebSocket receive handler
    async def websocket_receive(self, event):
        # Get the message from the event
        message = event.get("text")
        # Skip if message is empty
        if not message:
            return
        # JSON load (safe assumption frontend sends JSON)
        data = json.loads(message)
        username = data.get("username") or "Anonymous"
        text = data.get("message") or ""

        # empty message skip
        if text.strip() == "":
            return
    
        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "username": username,
                "message": text,
            }
        )


    # Chat message handler
    async def chat_message(self, event):
        # Send the message to the client
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({
                "username": event["username"],
                "message": event["message"],
            })
        })


    # WebSocket disconnect handler
    async def websocket_disconnect(self, event):
        # Remove this channel from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Print disconnect status
        print("Disconnected:", self.channel_name)