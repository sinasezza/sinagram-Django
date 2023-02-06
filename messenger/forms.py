from email import message
from django import forms
from . import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupForm(forms.Form):

    Choices = {
        ('male','Male'),
        ('female','Female'),
        ('others','Others'),
    }

    username    = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'required'}))
    # -----------------------------------
    password1   = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'required'}), label='Enter password',)
    # -----------------------------------
    password2   = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'required'}), label='Confirm password')
    # -----------------------------------
    first_name  = forms.CharField(label='first name',widget=forms.TextInput(attrs={'placeholder':'required'}))
    # -----------------------------------
    last_name   = forms.CharField(label='last name',required=False)
    # -----------------------------------
    gender      = forms.ChoiceField(label='gender' , choices=Choices,required=False)
    # -----------------------------------
    age   = forms.CharField(label='age',required=False)
    # -----------------------------------
    ssn   = forms.CharField(max_length=10 , label='ssn',widget=forms.TextInput(attrs={'placeholder':'required'}))
    # -----------------------------------
    email       = forms.CharField(widget=forms.EmailInput(),label='email',required=False)
    # -----------------------------------
    phone_number= forms.CharField(max_length=11 , label='phone number',widget=forms.TextInput(attrs={'placeholder':'required'}))
    # -----------------------------------
    photo     = forms.ImageField(widget=forms.FileInput(),label='photo' , required=False)
    # -----------------------------------
    about     = forms.CharField(label='about',widget=forms.Textarea(),required=False)
    # -----------------------------------

    def clean_username(self):
        username = self.cleaned_data.get('username')
        for user in User.objects.all():
            if username == user.username:
                raise forms.ValidationError('this username is already exist , try another')
        return username

    # -----------------------------------

    def clean_email(self):
        email = self.cleaned_data.get('email')
        for user in User.objects.all():
            if email == user.email:
                raise forms.ValidationError('this email is already used , please enter another email')
        return email
    
    # -----------------------------------

    def clean_phone_number(self):
        phone_num = self.cleaned_data.get('phone_number')
        for user in models.Account.objects.all() :
            if phone_num == user.user_phone_number:
                raise forms.ValidationError('the phone number entered is exists , enter another')
        return phone_num

    # -----------------------------------
    

# ======================================
# ======================================


class LoginForm(forms.Form):

    username   =  forms.CharField()
    # -----------------------------------
    password   =  forms.CharField(widget=forms.PasswordInput)


# ======================================
# ======================================


class AccountChangeInfoForm(forms.Form):

    Choices = {
        ('male','Male'),
        ('female','Female'),
        ('others','Others'),
    }
    
    # -----------------------------------
    user_id         = forms.IntegerField(label='id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)
    # -----------------------------------
    new_username    = forms.CharField(label='username')
    # -----------------------------------
    old_password    = forms.CharField(widget=forms.PasswordInput(), label='old password')
    # -----------------------------------
    new_password1   = forms.CharField(widget=forms.PasswordInput(), label='new password')
    # -----------------------------------
    new_password2   = forms.CharField(widget=forms.PasswordInput(), label='confirm password')
    # -----------------------------------
    new_first_name  = forms.CharField(label='first_name')
    # -----------------------------------
    new_last_name   = forms.CharField(label='last_name')
    # -----------------------------------
    new_gender      = forms.ChoiceField(label='gender' , choices=Choices)
    # -----------------------------------
    new_age         = forms.CharField(label='age')
    # -----------------------------------
    new_ssn         = forms.CharField(max_length=10,label='ssn')
    # -----------------------------------
    new_email       = forms.CharField(label='email',widget=forms.EmailInput())
    # -----------------------------------
    new_phone_number= forms.CharField(max_length=11 , label='phone_number')
    # -----------------------------------
    new_photo       = forms.ImageField(label='photo' , required=False)
    # -----------------------------------
    new_about       = forms.CharField(label='about',widget=forms.Textarea())
    # -----------------------------------

    def clean_new_username(self):
        username = self.cleaned_data.get('new_username')
        user_id = self.cleaned_data.get('user_id')
        for user in User.objects.exclude(id__exact = user_id):
            if username == user.username :
                raise forms.ValidationError('this username is already exist , enter another')
        return username

    # -----------------------------------

    def clean_new_email(self):
        email = self.cleaned_data.get('new_email')
        theusername = self.cleaned_data.get('new_username')
        for user in User.objects.exclude(username__exact = theusername):
            if email == user.email :
                raise forms.ValidationError('this email is already used , please enter another email')
        return email
        
    # -----------------------------------

    def clean_new_phone_number(self):
        phone_num = self.cleaned_data.get('new_phone_number')
        theuserid = self.cleaned_data.get('user_id')
        for user in models.Account.objects.exclude(id__exact = theuserid):
            if phone_num == user.user_phone_number:
                raise forms.ValidationError('the phone number entered is exists , enter another')
        return phone_num
        
    # -----------------------------------


# ======================================
# ======================================


class DeleteUserForm(forms.Form):
    
    yes = forms.CharField(widget=forms.HiddenInput(attrs={'value':1}) ,label='yes',required=False)
    

# ======================================
# ======================================


class LogoutForm(forms.Form):

    yes = forms.CharField(widget=forms.HiddenInput(attrs={'value':'1'}) ,label='yes',required=True)


# ======================================
# ======================================


class AddContactForm(forms.Form):

    account_id         = forms.IntegerField(label='account id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)
    # -----------------------------------
    first_name      = forms.CharField(label='first name (Required)',max_length=20,widget=forms.TextInput(attrs={'autofocus':True}),)
    # -----------------------------------
    last_name       = forms.CharField(label='last name',max_length=30,required=False)
    # -----------------------------------
    phone_number    = forms.CharField(label='phone number (Required)',max_length=11)
    # -----------------------------------
    email           = forms.CharField(label='email',widget=forms.EmailInput(),required=False)
    # -----------------------------------

    def clean_phone_number(self):
        number = self.cleaned_data.get('phone_number')
        account_id   = self.cleaned_data.get('account_id')
        for contact in models.Contact.objects.filter(Account_id__exact = account_id):
            if contact.phone_number == number:
                raise forms.ValidationError('this phone number registered before , please check that OR enter another phone number')
        return number


# ======================================
# ======================================


class DeleteContactForm(forms.Form):
    
    yes = forms.CharField(widget=forms.HiddenInput(attrs={'value':'1',}) ,label='yes',required=False)
    

# ======================================
# ======================================

class ContactChangeInfo(forms.Form):

    user_id         = forms.IntegerField(label='user_id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)    
    # -----------------------------------
    contact_id      = forms.IntegerField(label='contact_id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)
    # -----------------------------------
    fname           = forms.CharField(label='first name',max_length=20,widget=forms.TextInput(attrs={'autofocus':True}),)
    # -----------------------------------
    lname           = forms.CharField(label='last name',max_length=30 , required=False)
    # -----------------------------------
    phone_number    = forms.CharField(label='phone number',max_length=11)
    # -----------------------------------
    email           = forms.EmailField(label='email',widget=forms.EmailInput(),required=False)
    # -----------------------------------

    def clean_phone_number(self):
        number = self.cleaned_data.get('phone_number')
        user_id = self.cleaned_data.get('user_id')
        contact_id = self.cleaned_data.get('contact_id')
        for contact in models.Contact.objects.filter(Account_id__exact=user_id).exclude(id__exact=contact_id):
            if contact.phone_number == number:
                raise forms.ValidationError('this phone number already exists in your contacts , please check OR try another number ...')
        return number


# ======================================
# ======================================


class SendMessageForm(forms.Form):
    
    sender_id   = forms.IntegerField(label='sender_id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)
    # -----------------------------------
    receiver_id = forms.IntegerField(label='receiver_id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)
    # -----------------------------------
    file        = forms.FileField(label='file',required=False)
    # -----------------------------------
    message     = forms.CharField(label='message',required=False,max_length=500,widget=forms.Textarea(attrs={'autofocus':True,'rows':2,'cols':70,'id':'id_text','style':'resize:none;',}))


# ======================================
# ======================================



    