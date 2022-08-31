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

    username    = forms.CharField(label='username')
    # -----------------------------------
    password1   = forms.CharField(widget=forms.PasswordInput(), label='entered password')
    # -----------------------------------
    password2   = forms.CharField(widget=forms.PasswordInput(), label='confirm password')
    # -----------------------------------
    first_name  = forms.CharField(label='first_name')
    # -----------------------------------
    last_name   = forms.CharField(label='last_name')
    # -----------------------------------
    gender      = forms.ChoiceField(label='gender' , choices=Choices)
    # -----------------------------------
    age   = forms.CharField(label='age')
    # -----------------------------------
    ssn   = forms.CharField(max_length=10 , label='ssn')
    # -----------------------------------
    email       = forms.CharField(widget=forms.EmailInput(),label='email')
    # -----------------------------------
    phone_number= forms.CharField(max_length=11 , label='phone_number',)
    # -----------------------------------
    photo     = forms.ImageField(widget=forms.FileInput(),label='photo' , required=False)
    # -----------------------------------
    about     = forms.CharField(label='about',widget=forms.Textarea())
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


class ChangeInfoForm(forms.Form):

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
    new_email       = forms.CharField(label='email')
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
            else :
                print('the phone is {}'.format(user.user_phone_number))
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