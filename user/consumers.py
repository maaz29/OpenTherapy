import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User, TherapyRequest
from channels.db import database_sync_to_async


class TherapistConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.roomGroupName = "availableTherapists"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name,
        )
        await self.accept()

    async def send_updated_list(self, event):
        action = event["action"]
        active_therapists = await self.get_active_therapists()
        await self.send(text_data=json.dumps(
            {
                "therapists": active_therapists,
            }
        ))

    @database_sync_to_async
    def get_active_therapists(self):
        active_therapists = User.objects.filter(is_online=True)

        requests_by_client = TherapyRequest.objects.filter(client=self.scope['user'].username)

        if requests_by_client:
            list_of_requested_therapists = requests_by_client.values_list('therapist', flat=True)
            requested_therapists = list(list_of_requested_therapists)
        else:
            requested_therapists = []

        active_therapists = [{"username": obj.username,
                              "first_name": obj.first_name,
                              "last_name": obj.last_name,
                              "age": obj.age if obj.age is not None else "",
                              "city": obj.city if obj.city is not None else "",
                              "country": obj.country if obj.country is not None else "",
                              "profile_image": obj.profile_image.url,
                              "requested_therapists": requested_therapists
                              } for obj in active_therapists]
        return active_therapists

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "send.updated.list",
                "action": action
            })


class RequestsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.roomGroupName = "requestedSessions"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name,
        )
        await self.accept()

    async def send_request_list(self, event):
        action = event["action"]
        requested_therapists = await self.get_requests()
        await self.send(text_data=json.dumps(
            {
                "therapists": requested_therapists,
            }
        ))

    @database_sync_to_async
    def get_requests(self):
        all_requests = TherapyRequest.objects.filter(client=self.scope['user'].username)
        therapists_requested = []
        for req in all_requests:
            therapist = User.objects.get(username=req.therapist)
            session = TherapyRequest.objects.get(client=self.scope['user'].username, therapist=therapist.username)
            therapists_requested.append({'data': therapist, 'status': session.status, 'duration': session.duration})

        therapists_requested = [{
            "username": obj['data'].username,
            "client_username": self.scope['user'].username,
            "first_name": obj['data'].first_name,
            "last_name": obj['data'].last_name,
            "duration": obj['duration'],
            "status": obj['status'],
            "city": obj['data'].city if obj['data'].city is not None else "",
            "country": obj['data'].country if obj['data'].country is not None else "",
            "profile_image": obj['data'].profile_image.url,
        } for obj in therapists_requested]
        print(therapists_requested[0]['client_username'])

        return therapists_requested

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "send.request.list",
                "action": action
            })


class ClientListConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.roomGroupName = "requestingClients"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name,
        )
        await self.accept()

    async def send_client_list(self, event):
        action = event["action"]
        requests_from_clients = await self.get_clients()
        await self.send(text_data=json.dumps(
            {
                "client": requests_from_clients,
            }
        ))

    @database_sync_to_async
    def get_clients(self):
        all_requesting_clients = (TherapyRequest.objects.filter(therapist=self.scope['user'].username)
                                  .exclude(status='declined'))
        requests_from_clients = []
        for req in all_requesting_clients:
            client = User.objects.get(username=req.client)
            requests_from_clients.append(client)

        requests_from_clients = [{"username": obj.username,
                                  "first_name": obj.first_name,
                                  "last_name": obj.last_name,
                                  "city": obj.city if obj.city is not None else "",
                                  "country": obj.country if obj.country is not None else "",
                                  "profile_image": obj.profile_image.url,
                                  } for obj in requests_from_clients]

        return requests_from_clients

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action")
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "send.client.list",
                "action": action
            })
