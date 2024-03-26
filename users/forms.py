from typing import Any
from django import forms
from . import models
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

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
    phone_number = PhoneNumberField(max_length=13 , label='phone number',widget=forms.TextInput(attrs={'placeholder':'required'}))
    # -----------------------------------
    photo = forms.ImageField(widget=forms.FileInput(),label='photo' , required=False)
    # -----------------------------------
    about = forms.CharField(label='about',widget=forms.Textarea(),required=False)
    # -----------------------------------
    
    class Meta:
        model = models.UserProfile
        fields = ('gender', 'phone_number', 'age', 'about', 'photo',)

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
# ======================================


class AccountChangeInfoForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        fields = ('age', 'about', 'phone_number', 'gender', 'image')

    def __init__(self, *args, **kwargs):
        super(AccountChangeInfoForm, self).__init__(*args, **kwargs)
        # Add user-related fields from the User model
        self.fields['username'] = forms.CharField(label='Username', initial=self.instance.user.username, disabled=True)
        self.fields['email'] = forms.EmailField(label='Email', initial=self.instance.user.email, disabled=True)
        self.fields['first_name'] = forms.CharField(label='First Name', initial=self.instance.user.first_name)
        self.fields['last_name'] = forms.CharField(label='Last Name', initial=self.instance.user.last_name)

    def save(self, commit=True):
        user_profile = super(AccountChangeInfoForm, self).save(commit=False)
        # Update user-related fields from the User model
        user_profile.user.first_name = self.cleaned_data['first_name']
        user_profile.user.last_name = self.cleaned_data['last_name']
        if commit:
            user_profile.save()
            user_profile.user.save()
        return user_profile
        



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











    