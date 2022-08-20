from django.db import models
from django.contrib.auth import get_user_model


class Account(models.Model):

    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
    # -----------------------------------
    user_age                 = models.PositiveSmallIntegerField(null=True , blank=True , )
    # -----------------------------------
    user_ssn                 = models.CharField(max_length=10 , null=True , blank=True , )
    # -----------------------------------
    user_about               = models.CharField(max_length=500 , null=True , blank=True)
    # -----------------------------------
    user_phone_number        = models.CharField(max_length=11)
    # -----------------------------------
    user_photo               = models.ImageField(upload_to= 'uploads/', null=True , blank=True)
    # -----------------------------------