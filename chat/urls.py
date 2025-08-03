from django.urls import path
from . import views

urlpatterns = [
    path(r"chat-room/<str:room_name>", views.chat_page, name="chat-page"),
    path(r"end-session", views.end_session, name="end-session")
]
