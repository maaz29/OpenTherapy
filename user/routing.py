from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("ws/user/client/dashboard", consumers.TherapistConsumer.as_asgi()),
    path("ws/user/client/requests", consumers.RequestsConsumer.as_asgi()),
    path("ws/user/therapist/dashboard", consumers.ClientListConsumer.as_asgi()),
]
