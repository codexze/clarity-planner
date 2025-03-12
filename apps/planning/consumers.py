import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PlanningConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("planning", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("planning", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send("planning", {
            "type": "send_task_update",
            "message": data["message"],
        })

    async def send_task_update(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))