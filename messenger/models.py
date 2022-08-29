from django.db import models 
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
import datetime


class Account(models.Model):

    class Meta:
        unique_together = ('user','user_phone_number',)

    def user_directory_path(instance, filename):
        year  = datetime.date.today().year
        month = datetime.date.today().month
        day   = datetime.date.today().day
        return 'uploads/{0}/{1}/{2}/{3}/{4}'.format(year,month,day,instance.user.username,filename)

    # -----------------------------------

    Choices = {
        ('male','Male'),
        ('female','Female'),
        ('others','Others'),
    }
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,primary_key=True)
    # -----------------------------------
    user_age                 = models.PositiveSmallIntegerField(null=True , blank=True , )
    # -----------------------------------
    user_ssn                 = models.CharField(max_length=10 , null=True , blank=True , )
    # -----------------------------------
    user_about               = models.CharField(max_length=500 , null=True , blank=True)
    # -----------------------------------
    user_phone_number        = models.CharField(max_length=11)
    # -----------------------------------
    user_photo               = models.ImageField(upload_to= user_directory_path, null=True , blank=True)
    # -----------------------------------
    user_gender              = models.CharField(max_length=6,choices=Choices,null=True,blank=True)

    def get_panel_url(self):
        return reverse('messenger:panel',args=[self.user.username])

    # -----------------------------------
    
    @property
    def user_email(self):
        return self.user.email

