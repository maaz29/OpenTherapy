import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = str(self.scope["url_route"]["kwargs"]["room_name"])
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        duration = text_data_json.get("duration")
        profile_image = text_data_json.get("profile_image")
        first_name = text_data_json.get("first_name")

        if duration:
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "send_session_duration",
                    "duration": duration,
                })
        else:
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "send.message",
                    "message": message,
                    "username": username,
                    "profile_image": profile_image,
                    "first_name": first_name,
                })

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        profile_image = event["profile_image"]
        first_name = event["first_name"]
        await self.send(text_data=json.dumps({"message": message,
                                              "username": username,
                                              "profile_image": profile_image,
                                              "first_name": first_name}
                                             ))

    async def send_session_duration(self, event):
        duration = event["duration"]
        if duration:
            await self.send(text_data=json.dumps({"duration": duration}))
