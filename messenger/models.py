from django.db import models 
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone , dateformat



class Account(models.Model):

    class Meta:
        unique_together = ('id','user','user_phone_number',)

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
    user_photo               = models.ImageField(upload_to= user_directory_path, null=True , blank=True)
    # -----------------------------------
    user_gender              = models.CharField(max_length=6,choices=Choices,null=True,blank=True)
    # -----------------------------------

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


# ======================================
# ======================================

class Contact(models.Model):

    class Meta:
        unique_together = ('Account','phone_number')

    Account         = models.ForeignKey(to='messenger.Account',on_delete=models.CASCADE)
    # -----------------------------------
    fname           = models.CharField(max_length=20)
    # -----------------------------------
    lname           = models.CharField(default='',max_length=30 , null=True , blank=True)
    # -----------------------------------
    phone_number    = models.CharField(max_length=11)
    # -----------------------------------
    email           = models.EmailField(default='',null=True,blank=True)


    def __str__(self):
        return '{}\'s contact : {}'.format(self.Account.user.username,self.fullname)

    # -----------------------------------

    @property
    def username(self):
        return self.Account.user.username
    
    # -----------------------------------

    @property
    def fullname(self):
        if self.lname == None:
            return self.fname
        return self.fname + ' ' + self.lname

    # -----------------------------------

    def get_contact_url(self):
        return reverse('messenger:contact_detail',args=[self.username,self.fullname,self.id])
    
    # -----------------------------------
    

# ======================================
# ======================================


class Message(models.Model):
    
    sender   = models.ForeignKey(to=Account,on_delete=models.DO_NOTHING,related_name='sender')
    # -----------------------------------
    receiver = models.ForeignKey(to=Account,on_delete=models.DO_NOTHING,related_name='receiver')
    # -----------------------------------
    content  = models.FileField(upload_to='content/',null=True,blank=True)
    # -----------------------------------
    message  = models.TextField(max_length=500,null=True , blank=True)
    # -----------------------------------
    sent_date= models.DateTimeField(default=dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
    # -----------------------------------

    def __str__(self):
        return 'massage_id ({}) - from {} to {}'.format(self.id,self.sender,self.receiver)

    # -----------------------------------
