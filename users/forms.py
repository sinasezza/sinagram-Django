from typing import Any
from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from django.db.models import Q
from . import models

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Enter the your password.",
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Enter the same password as before, for verification.",
    )
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if (User.objects.filter(username=username).exists()):
            raise forms.ValidationError('The username is already taken. please  choose a different one.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise forms.ValidationError('Your password must be at least 8 characters long.')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('passwords not math.')
        return password2
    
    def save(self, commit: bool = True) -> Any:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

    # -----------------------------------


class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(label='gender', choices=models.UserProfile.GENDER_CHOICES, required=False)
    # -----------------------------------
    age = forms.CharField(label='age', required=False, widget=forms.NumberInput(attrs={'type':'number', 'min': 0, 'max': 99}))
    # -----------------------------------
    phone_number = PhoneNumberField(max_length=13, label='phone number',widget=forms.TextInput(attrs={'placeholder':'required'}))
    # -----------------------------------
    image = forms.ImageField(widget=forms.FileInput(),label='image' , required=False)
    # -----------------------------------
    about = forms.CharField(label='about', widget=forms.Textarea(), required=False)
    # -----------------------------------
    
    class Meta:
        model = models.UserProfile
        fields = ('gender', 'phone_number', 'age', 'about', 'image',)

    # -----------------------------------

    def clean_phone_number(self):
        phone_num = self.cleaned_data.get('phone_number')
        if models.UserProfile.objects.filter(phone_number=phone_num).exists() :
            raise forms.ValidationError('the phone number entered is exists , enter another')
        return phone_num

    # -----------------------------------
    


class LoginForm(forms.Form):

    username   =  forms.CharField()
    # -----------------------------------
    password   =  forms.CharField(widget=forms.PasswordInput)


# ======================================


class AccountChangeForm(forms.ModelForm):
    username = forms.CharField(label='Username', disabled=True)    

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


    def clean(self):
        cleaned_data = super().clean()        
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
                
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This username is already exist, enter another')
    
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This email is already used, please enter another email')
    

# ======================================

class ProfileChangeForm(forms.ModelForm):
    phone_number = PhoneNumberField(max_length=13, label='Phone Number', widget=forms.TextInput(attrs={'placeholder': 'Required'}))

    class Meta:
        model = models.UserProfile
        fields = ('age', 'about', 'phone_number', 'gender', 'image')

    def clean(self):
        cleaned_data = super().clean()
        phone_num = cleaned_data.get('phone_number')

        if models.UserProfile.objects.filter(phone_number=phone_num).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('The phone number entered already exists, enter another')

        return cleaned_data

# ======================================


class DeleteUserForm(forms.Form):
    
    yes = forms.CharField(widget=forms.HiddenInput(attrs={'value':1}) ,label='yes',required=False)
    

# ======================================


class LogoutForm(forms.Form):

    yes = forms.CharField(widget=forms.HiddenInput(attrs={'value':'1'}) ,label='yes',required=True)


# ======================================


class ContactAddForm(forms.ModelForm):

    fname      = forms.CharField(label='first name (Required)', max_length=20, widget=forms.TextInput(attrs={'autofocus':True}),)
    lname       = forms.CharField(label='last name', max_length=30, required=False)
    phone = PhoneNumberField(max_length=13, label='Phone Number (Required)', widget=forms.TextInput(attrs={'placeholder': 'Required'}))
    email           = forms.CharField(label='email' ,widget=forms.EmailInput(), required=False)
    image = forms.ImageField(label='image',  required=False)
    
    class Meta:
        model = models.Contact
        fields = ('fname', 'lname', 'phone', 'email', 'image',)
    

    def clean_phone(self):
        number = self.cleaned_data.get('phone')
        
        if models.Contact.objects.filter(phone=number).exists():
            raise forms.ValidationError('this phone number registered before , please check that OR enter another phone number')
        else:
            print(f"the number {number} does not exists")
    
        return number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if models.Contact.objects.filter(email=email).exists():
            raise forms.ValidationError('this email registered before , please check that OR enter another email')

        return email



# ======================================

class ContactUpdateForm(forms.ModelForm):

    fname      = forms.CharField(label='first name (Required)', max_length=20, widget=forms.TextInput(attrs={'autofocus':True}),)
    lname       = forms.CharField(label='last name', max_length=30, required=False)
    phone = PhoneNumberField(max_length=13, label='Phone Number (Required)', widget=forms.TextInput(attrs={'placeholder': 'Required'}))
    email           = forms.CharField(label='email' ,widget=forms.EmailInput(), required=False)
    image = forms.ImageField(label='image',  required=False)
    
    class Meta:
        model = models.Contact
        fields = ('fname', 'lname', 'phone', 'email', 'image',)
    

    def clean_phone(self):
        number = self.cleaned_data.get('phone')
        
        if models.Contact.objects.filter(phone=number).exclude(phone=self.instance.phone).exists():
            raise forms.ValidationError('this phone number registered before , please check that OR enter another phone number')
    
        return number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email and models.Contact.objects.filter(email=email).exclude(email=self.instance.email).exists():
            raise forms.ValidationError('this email registered before , please check that OR enter another email')

        return email


# ======================================


class DeleteContactForm(forms.Form):
    yes = forms.CharField(widget=forms.HiddenInput(attrs={'value':'1',}) ,label='yes',required=False)
    
# ======================================











    