import json
from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . import models


class MessengerConsumer(AsyncWebsocketConsumer):
    pass