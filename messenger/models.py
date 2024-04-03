
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse
from django.conf import settings
from sinagram import utils as prj_utils
from users.models import UserProfile


class PublicRoom(models.Model):
    id = models.CharField(max_length=settings.DEFAULT_ID_LENGTH, primary_key=True, default=prj_utils.id_gen, editable=False)
    # -----------------------------------
    name = models.CharField(max_length=100, blank=True, null=True)  
    # -----------------------------------
    members = models.ManyToManyField(to=UserProfile, related_name='public_rooms')
    # -----------------------------------
    creator = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, related_name='my_public_rooms', blank=True, null=True)


    def __str__(self):
        return self.name


class PrivateRoom(models.Model):
    id = models.CharField(max_length=settings.DEFAULT_ID_LENGTH, primary_key=True, default=prj_utils.id_gen, editable=False)
    # -----------------------------------
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='private_rooms_user1', blank=True, null=True)
    # -----------------------------------
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='private_rooms_user2', blank=True, null=True)
    # -----------------------------------


    def __str__(self):
        return f"Private Room between {self.user1} and {self.user2}"
    
    def get_room_url(self):
        return reverse('messenger:contact-chat', kwargs={'room_id': self.id})


class Message(models.Model):
    public_room = models.ForeignKey(to=PublicRoom, on_delete=models.CASCADE, related_name='public_messages', blank=True, null=True)
    # -----------------------------------
    private_room = models.ForeignKey(to=PrivateRoom, on_delete=models.CASCADE, related_name='private_messages', blank=True, null=True)
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
