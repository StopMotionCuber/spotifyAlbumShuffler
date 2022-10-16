from channels.generic.websocket import AsyncWebsocketConsumer


class PlaylistUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.send({
            "type": "websocket.accept",
        })

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, code):
        pass
