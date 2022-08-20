from django import forms
from . import models

class SignupForm(forms.Form):

    class meta:
        model = models.Account

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
    age   = forms.CharField(label='age')
    # -----------------------------------
    ssn   = forms.CharField(label='ssn')
    # -----------------------------------
    email       = forms.CharField(label='email')
    # -----------------------------------
    phone_number= forms.CharField(max_length=11 , label='phone_number')
    # -----------------------------------
    # photo     = forms.ImageField(label='picture')

# ======================================
# ======================================


class LoginForm(forms.Form):

    username   =  forms.CharField()
    # -----------------------------------
    password   =  forms.CharField(widget=forms.PasswordInput)