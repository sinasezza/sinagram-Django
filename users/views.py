from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from . import models, forms, decorators


@decorators.logout_required
def signup_view(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Account registered successfully')
            return redirect('users:login')
        else:
            print(f"form error : {form.errors.as_data()}")
            messages.error(request, 'error in form fields')
    else:
        form = forms.SignupForm()


    return render(request, 'users/signup_page.html', {'form': form})


# ======================================

@decorators.logout_required
def login_view(request):
    if request.method == 'POST' :
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'hello {}'.format(user.username))
                    return redirect('index') if models.UserProfile.objects.filter(user=user).exists() else redirect('users:create-profile')
                else:
                    messages.error(request,'user in not active')
                    return redirect('index')
            else :
                messages.error(request,'username or password is wrong')
                # form  = forms.LoginForm()
    else :
        form = forms.LoginForm()

    context = {
        'form' : form,
    }

    return render(request,'users/login_page.html', context)

# ======================================

@login_required(login_url='users:login')
def Logout_view(request):
    logout(request)
    return redirect('users:login')

# ======================================

@login_required(login_url='users:login')
def create_profile_view(request):
    try:
        profile = models.UserProfile.objects.get(user=request.user)
    except:
        profile = None
        
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request,"Your Profile has been created")
            return redirect('index')
        else:
            messages.error(request, "Please correct the error below.")
    else:            
        form = forms.UserProfileForm(instance=profile)
        
    context = {
        'form': form,
    }
    
    return render(request,  'users/create_profile.html', context)

# ======================================

# @login_required
# def profile_view(request, username):
#     user = get_object_or_404(User, username=username)
#     followers = user.followers.all().count()
#     following = user.following.all().count()

# ======================================

@login_required(login_url='users:login')
@decorators.profile_required
def panel_view(request,username):
    user = User.objects.get(username__exact = username)
    usr = models.Account.objects.get(user__exact = user)
    context = {
        'usr':usr,
    }
    return render(request,'messenger_pages/panel.html',context)

# ======================================

@login_required(login_url='users:login')
@decorators.profile_required
def change_account_info_view(request,username):
    account = models.Account.objects.get(user__exact = request.user)
    if request.method == 'POST':
        form = forms.AccountChangeInfoForm(request.POST,request.FILES)
        if form.is_valid():    
            cd = form.cleaned_data      
            if not account.user.check_password(cd['old_password']):
                messages.error(request,'the password is wrong')
                return redirect('messenger:change_info',request.user.username)
            elif cd['new_password1'] != cd['new_password2'] :
                messages.error(request,'new passwords is not same')
                return redirect('messenger:change_info',request.user.username)
            else:
                account.user.set_password(cd['new_password1'])
                account.user.username   = cd['new_username']
                account.user.first_name = cd['new_first_name']
                account.user.last_name  = cd['new_last_name']
                account.user.email      = cd['new_email']
                account.user.save()
                
                account.user_phone_number   = cd['new_phone_number']
                account.user_gender         = cd['new_gender']
                account.user_age            = cd['new_age']
                account.user_ssn            = cd.get('new_ssn',account.user_ssn)
                if request.FILES.get('new_photo',None) is not None:
                    account.user_photo          = request.FILES.get('new_photo',False)
                account.user_about          = cd['new_about']
                account.save()

                login(request,User.objects.get(username__exact=username))
                messages.success(request,'updated successfully')
                return redirect(account.get_panel_url())  

        else:
            messages.error(request,'form is not valid')
            return render(request,'forms/change_account_info.html',{'form':form,})
    
    else:
        form = forms.AccountChangeInfoForm()
        form.fields['user_id'].initial          = request.user.id
        form.fields['new_username'].initial     = account.user.username
        form.fields['new_first_name'].initial   = account.user.first_name
        form.fields['new_last_name'].initial    = account.user.last_name
        form.fields['new_email'].initial        = account.user.email
        form.fields['new_phone_number'].initial = account.user_phone_number
        form.fields['new_gender'].initial       = account.user_gender
        form.fields['new_age'].initial          = account.user_age
        form.fields['new_ssn'].initial          = account.user_ssn
        form.fields['new_photo'].initial        = account.user_photo
        form.fields['new_about'].initial        = account.user_about
        return render(request,'forms/change_account_info.html',{'form':form,})

# ======================================

@login_required(login_url='messenger:main_page')
def delete_user_view(request,username):
    account = models.Account.objects.get(user__exact = request.user)
    if request.method == "POST":
        form = forms.DeleteUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yes'] == '1' :
                User.objects.get(username__exact=username).delete()
                messages.success(request,'account deleted successfully')
                return redirect('messenger:main_page')
            else:
                messages.error(request, 'the account deletion failed , please try again ...')
                return reverse_lazy(account.get_panel_url())
        else:
            messages.error(request,'form is not valid')
            return redirect('messenger:delete_user',request.user.username)
    else:
        form = forms.DeleteUserForm()
    
    context = {
        'form':form,
        'usr' : account,

    }
    return render(request,'forms/delete_user_form.html',context)

# ======================================

@login_required(login_url= 'users:login')
@decorators.profile_required
def contact_list_view(request,username):
    usr = models.Account.objects.get(user__exact = request.user)
    contacts = models.Contact.objects.filter(Account_id__exact = request.user.id)
    context = {
        'contacts':contacts,
        'usr':usr,
    }
    return render(request,'messenger_pages/contact_list.html',context)
 
# ======================================

@login_required(login_url='users:login')
@decorators.profile_required
def contact_detail_view(request,username,name,id):
    contact = models.Contact.objects.get(Account_id__exact= request.user.id , id__exact=id)
    try:
        contact_account = models.Account.objects.get(user_phone_number__exact = contact.phone_number)
        context = {
            'contact':contact,
            'account':contact_account,
        }
        
    except:
        context = {
            'contact':contact,
        }
        
    
    return render(request,'messenger_pages/contact_detail.html',context) 
        
# ======================================

@login_required(login_url= 'users:login')
@decorators.profile_required
def add_contact_view(request,username):
    
    usr = models.Account.objects.get(user__exact = request.user)
    if request.method == 'POST':
        form = forms.AddContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            contact = models.Contact.objects.create( Account=usr,
                                                     fname=cd.get('first_name'),
                                                     lname=cd.get('last_name'),
                                                     phone_number=cd.get('phone_number'),
                                                     email = cd.get('email'))
            contact.save()
            messages.success(request,'the contact added successfully')
            return redirect(usr.get_contacts_url())
        else:
            messages.error(request,'the form is invalid')
            return render(request,'forms/add_contact_page.html',{'form':form,'usr':usr,})
    else:
        form = forms.AddContactForm()
        form.fields['account_id'].initial = request.user.id
        
    return render(request,'forms/add_contact_page.html',{'form':form,'usr':usr,})

# ======================================

@login_required(login_url= 'users:login')
@decorators.profile_required
def change_contact_info_view(request,username,name,id):
    usr = models.Account.objects.get(user__exact =request.user)
    contact = models.Contact.objects.get(Account_id__exact= request.user.id , id__exact=id)
    if request.method == 'POST':
        form = forms.ContactChangeInfo(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            contact.fname = cd.get('fname')
            contact.lname  = cd.get('lname')
            contact.phone_number = cd.get('phone_number')
            contact.email = cd.get('email')
            contact.save()
            messages.success(request,'the contact Informations Updated')
            return redirect(contact.get_contact_url())
        else :
            messages.error(request,'the form is not valid')
            return render(request,'forms/change_contact_info.html',{'form':form,'usr':usr,'contact':contact,})        
    else:
        form = forms.ContactChangeInfo()
        form.fields['user_id'].initial = request.user.id
        form.fields['contact_id'].initial = id
        form.fields['fname'].initial = contact.fname
        form.fields['lname'].initial = contact.lname
        form.fields['phone_number'].initial = contact.phone_number
        form.fields['email'].initial = contact.email
    
    context = {
        'form':form,
        'usr':usr,
        'contact':contact,
    }
    return render(request,'forms/change_contact_info.html',context)

# ======================================

@login_required(login_url= 'users:login')
@decorators.profile_required
def delete_contact_view(request,username,name,id):
    usr = models.Account.objects.get(user__exact =request.user)
    contact = models.Contact.objects.get(Account_id__exact= request.user.id , id__exact=id)
    if request.method == 'POST':
        form = forms.DeleteContactForm(request.POST)
        if form.is_valid():
            print('\nvalue is : {}\n'.format(form.cleaned_data.get('yes')))
            if form.cleaned_data.get('yes') == '1':
                contact.delete()
                messages.success(request,'the contact deleted ...')
                return redirect(usr.get_contacts_url())
            else:
                messages.error(request,'the contact deletion failed , try again')
                return render(request,'forms/delete_contact_form.html',{'form':form,'usr':usr,})
        else :
            messages.error(request,'the form is not valid')
            return render(request,'forms/delete_contact_form.html',{'form':form,'usr':usr,'contact':contact,})        
    else:
        form = forms.DeleteContactForm()
    
    context = {
        'form':form,
        'usr':usr,
        'contact':contact,
    }
    return render(request,'forms/delete_contact_form.html',context)
