from django.urls import re_path
from messenger import consumers as messenger_consumers

websocket_urlpatterns = [
    re_path(r'ws/messenger/(?P<room_name>[\w-]+)/$', messenger_consumers.MessengerConsumer.as_asgi()),
]
