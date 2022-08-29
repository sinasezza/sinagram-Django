from django import forms
from . import models
from django.contrib.auth.models import User

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
    phone_number= forms.CharField(max_length=11 , label='phone_number')
    # -----------------------------------
    photo     = forms.ImageField(widget=forms.FileInput(),label='photo' , required=False)
    # -----------------------------------
    about     = forms.CharField(label='about')

    def clean_email(self):
        email = self.email
        for user in User.objects.all():
            if email == user.email:
                raise forms.ValidationError('this email is already used , please enter another email')
        return email

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
    new_about       = forms.CharField(label='about')
    # -----------------------------------

    def check_photo(self):
        if self.new_photo is not None:
            return self.new_photo
        else:
            print('***\n\n\nthe photo is None \n\n\n***')
   
    # -----------------------------------

    def clean_email(self):
        email = self.email
        for user in User.objects.all():
            if email == user.email:
                raise forms.ValidationError('this email is already used , please enter another email')
        return email

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