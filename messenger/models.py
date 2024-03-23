
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from sinagram import utils as prj_utils
from users.models import UserProfile


class PublicRoom(models.Model):
    id = models.CharField(max_length=settings.DEFAULT_ID_LENGTH, primary_key=True, default=prj_utils.id_gen, editable=False)
    # -----------------------------------
    name = models.CharField(max_length=100, blank=True, null=True)  
    # -----------------------------------
    messages = GenericRelation(to='Message', object_id_field='id', content_type_field='room_type')

    def __str__(self):
        return self.name


class PrivateRoom(models.Model):
    id = models.CharField(max_length=settings.DEFAULT_ID_LENGTH, primary_key=True, default=prj_utils.id_gen, editable=False)
    # -----------------------------------
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='private_rooms_user1', blank=True, null=True)
    # -----------------------------------
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='private_rooms_user2', blank=True, null=True)
    # -----------------------------------
    messages = GenericRelation(to='Message', object_id_field='id', content_type_field='room_type')

    def __str__(self):
        return f"Private Room between {self.user1} and {self.user2}"


class Message(models.Model):
    room_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    # -----------------------------------
    room_id = models.CharField(max_length=settings.DEFAULT_ID_LENGTH, blank=True, null=True)
    # -----------------------------------
    room_object = GenericForeignKey('room_type', 'room_id')
    # -----------------------------------
    sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='sent_messages', null=True, blank=True)
    # -----------------------------------
    receiver = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='received_messages', null=True, blank=True)
    # -----------------------------------
    content = models.FileField(upload_to='messenger/contents/', null=True, blank=True)
    # -----------------------------------
    message = models.TextField(max_length=500, null=True, blank=True)
    # -----------------------------------
    sent_date = models.DateTimeField(auto_now_add=True)
    # -----------------------------------

    def __str__(self):
        return f'Message {self.id} - from {self.sender} to {self.receiver}'
