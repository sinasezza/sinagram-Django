from django.db import models 
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone , dateformat
from users.models import UserProfile


class PrivateRoom(models.Model):
    pass

class PublicRoom(models.Model):
    pass

class Message(models.Model):
    
    sender   = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, related_name='sender', null=True, blank=True,)
    # -----------------------------------
    receiver = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, related_name='receiver', null=True, blank=True)
    # -----------------------------------
    content  = models.FileField(upload_to='messenger/contents/', null=True, blank=True)
    # -----------------------------------
    message  = models.TextField(max_length=500,null=True , blank=True)
    # -----------------------------------
    sent_date= models.DateTimeField(default=dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
    # -----------------------------------

    def __str__(self):
        return 'massage_id ({}) - from {} to {}'.format(self.id,self.sender,self.receiver)

    # -----------------------------------
