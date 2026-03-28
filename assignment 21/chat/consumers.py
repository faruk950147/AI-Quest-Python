from channels.consumer import AsyncConsumer
import json

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("received", event)

        text_data = event.get("text", None)

        if text_data:
            try:
                data = json.loads(text_data)
                message = data.get("message", "")
            except:
                message = text_data  # fallback

            await self.send({
                "type": "websocket.send",
                "text": f"Echo: {message}"
            })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        await self.send({
            "type": "websocket.close"
        })
