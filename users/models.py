from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from sinagram import utils as prj_utils
from django.urls import reverse
from django.db import models



class UserProfile(models.Model):

    def user_directory_path(instance, filename):
        year  = datetime.date.today().year
        month = datetime.date.today().month
        day   = datetime.date.today().day
        return 'users/img/{0}/{1}/{2}/{3}/{4}'.format(year,month,day,instance.user.username,filename)

    # -----------------------------------

    Choices = {
        ('male','Male'),
        ('female','Female'),
        ('others','Others'),
    }
    
    id = models.CharField(max_length=settings.DEFAULT_ID_LENGTH, primary_key=True, default=prj_utils.id_gen, editable=False)
    # -----------------------------------
    user = models.OneToOneField(to=User ,on_delete=models.CASCADE)
    # -----------------------------------
    age           = models.CharField(max_length=2, null=True, blank=True, default='0')
    # -----------------------------
    about         = models.TextField(max_length=500, null=True, blank=True)
    # -----------------------------
    phone_number  = models.CharField(max_length=11, unique=True,)
    # -----------------------------
    image         = models.ImageField(upload_to= user_directory_path, null=True , blank=True)
    # -----------------------------
    gender        = models.CharField(max_length=6, choices=Choices, default='others')
    # -----------------------------------
    contacts = models.ManyToManyField(to='UserProfile', blank=True)
    

    def get_panel_url(self):
        return reverse('messenger:panel',args=[self.user.username])

    # -----------------------------------
    
    @property
    def user_email(self):
        return self.user.email

    # -----------------------------------

    def get_contacts_url(self):
        return reverse('messenger:contacts',args=[self.user.username])

    # -----------------------------------

    def get_add_contact_url(self):
        return reverse('messenger:add_contact',args=[self.user.username])

    # -----------------------------------

    def get_chat_page(self):
        return reverse('messenger:contact_chat',args=[self.user.id])

    # -----------------------------------

    def __str__(self):
        return self.user.username


