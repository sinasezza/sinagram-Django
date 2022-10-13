from django.shortcuts import render , redirect , HttpResponse , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout  
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core import serializers
import json
from django.forms.models import model_to_dict

from . import models,forms
# from rest_framework.decorators import api_view


def main_page(request):
    usr = None
    if request.user.is_authenticated:
        usr = models.Account.objects.get(user__exact = request.user)

    content = {
        'usr' : usr,
    }
    return render(request , 'Home/main_page.html',content)

# ======================================

def signup_view(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already loged in , please log out and try again')
        return redirect('messenger:main_page')
    if request.method == 'POST':
        form = forms.SignupForm(request.POST , request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password1'] != cd['password2']:
                messages.error('passwords are not same')
                return redirect('accounts:signup')
            newUser = User( username=cd['username'],
                            first_name=cd['first_name'],
                            last_name=cd['last_name'],
                            email=cd['email'])
            newUser.set_password(cd['password1'])
            newUser.save()
            newAccount =  models.Account(   user=newUser,
                                            user_gender=cd['gender'],
                                            user_age=cd['age'],
                                            user_ssn=cd['ssn'],
                                            user_phone_number=cd['phone_number'],
                                            user_photo=cd['photo'],
                                            user_about=cd['about'],)
            newAccount.save()
            messages.success(request ,'account registered successfully')
            return redirect('messenger:main_page')
        else:
            messages.error(request,'form is not valid')
            return render(request,'forms/signup_page.html',{'form':form,})
        
    else:
        form = forms.SignupForm()
        return render(request,'forms/signup_page.html',{'form':form,})


# ======================================

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already loged in , please log out and try again')
        return redirect('messenger:main_page')
    if request.method == 'POST' :
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'hello {}'.format(user.username))
                    return redirect('messenger:main_page')
                else:
                    messages.error(request,'user in not active')
                    return redirect('messenger:login')
            else :
                messages.error(request,'username or password is wrong')
                return redirect('messenger:login')
    else :
        form = forms.LoginForm()

    content = {
        'form' : form,
    }

    return render(request,'forms/login_page.html',content)

# ======================================

@login_required(login_url='messenger:login')
def Logout_view(request):
    user = User.objects.get(username__exact = request.user.username)
    usr = models.Account.objects.get(user__exact = user)
    if request.method == 'POST':
        form = forms.LogoutForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('yes') == '1':
                logout(request)
                messages.success(request, "Logged Out Successfully!!")
                return redirect('messenger:main_page')
            else:
                messages.error(request,'logout failed')
                return redirect('messenger:logout')
        else:
            messages.error(request,'form is not valid')
            return redirect('messenger:logout')
    else:
        form = forms.LogoutForm()
    
    content = {
        'usr':usr,
        'form':form ,
    }
    return render(request,'forms/logout_page.html',content)

# ======================================

@login_required(login_url='messenger:login')
def panel_view(request,username):
    user = User.objects.get(username__exact = username)
    usr = models.Account.objects.get(user__exact = user)
    content = {
        'usr':usr,
    }
    return render(request,'messenger_pages/panel.html',content)

# ======================================

@login_required(login_url='messenger:login')
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
    
    content = {
        'form':form,
        'usr' : account,

    }
    return render(request,'forms/delete_user_form.html',content)

# ======================================

@login_required(login_url= 'messenger:login')
def contact_list_view(request,username):
    usr = models.Account.objects.get(user__exact = request.user)
    contacts = models.Contact.objects.filter(Account_id__exact = request.user.id)
    content = {
        'contacts':contacts,
        'usr':usr,
    }
    return render(request,'messenger_pages/contact_list.html',content)
 
# ======================================

@login_required(login_url='messenger:login')
def contact_detail_view(request,username,name,id):
    contact = models.Contact.objects.get(Account_id__exact= request.user.id , id__exact=id)
    try:
        contact_account = models.Account.objects.get(user_phone_number__exact = contact.phone_number)
        content = {
            'contact':contact,
            'account':contact_account,
        }
        
    except:
        content = {
            'contact':contact,
        }
        
    
    return render(request,'messenger_pages/contact_detail.html',content) 
        
# ======================================

@login_required(login_url= 'messenger:login')
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

@login_required(login_url= 'messenger:login')
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
    
    content = {
        'form':form,
        'usr':usr,
        'contact':contact,
    }
    return render(request,'forms/change_contact_info.html',content)

# ======================================

@login_required(login_url= 'messenger:login')
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
    
    content = {
        'form':form,
        'usr':usr,
        'contact':contact,
    }
    return render(request,'forms/delete_contact_form.html',content)

# ======================================

@login_required(login_url= 'messenger:login')
def contact_chat_view(request,id):
    sender = models.Account.objects.get(id__exact = request.user.id)
    receiver = models.Account.objects.get(id__exact = id)

    if request.method == 'POST':
        form = forms.SendMessageForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            message = models.Message.objects.create(  sender=sender ,
                                            receiver=receiver,
                                            message=cd['message'])
            message.save()
            return JsonResponse(make_data_message([message,]),safe=False)
        else:
            messages.error(request,'form is not valid')

    else :
            form = forms.SendMessageForm()
            form.fields['sender_id'].initial = sender.id
            form.fields['receiver_id'].initial = receiver.id
            return render(request,'messenger_pages/contact_chat_page.html',context={'form':form,})

# =====================================

@login_required(login_url = 'messenger:login')
def get_message_numbers(request,id):
    all_messages = models.Message.objects.filter(sender_id__exact=id,receiver_id__exact=request.user.id) | \
        models.Message.objects.filter(sender_id__exact=request.user.id,receiver_id__exact=id)
    return HttpResponse(all_messages.count())

# =====================================

@login_required(login_url= 'messenger:login')
def get_all_messages(request,id):

    all_messages = models.Message.objects.filter(sender_id__exact=id,receiver_id__exact=request.user.id) | \
        models.Message.objects.filter(sender_id__exact=request.user.id,receiver_id__exact=id)
    all_messages = all_messages.order_by('id')
    return JsonResponse(make_data_message(all_messages),safe=False)

# =====================================

@login_required(login_url= 'messenger:login')
def delete_message(request,id):
    if request.method == 'POST':
        instance = get_object_or_404(models.Message,id__exact =id)
        instance.delete()
    return HttpResponse(id)

# =====================================

@login_required(login_url= 'messenger:login')
def edit_message_view(request,id):
    theMessage = models.Message.objects.get(id__exact=id)
    if request.method == 'POST':
        theMessage.message = request.POST['msg']
        theMessage.save()
    data = make_data_message([theMessage,])
    return JsonResponse(data,safe=False)

# =====================================

def make_data_message(messages):
    data = []
    for i in range(len(messages)):
        data.append({
            'id':messages[i].id,
            'sender':messages[i].sender.user.username,
            'message':messages[i].message,
            'sent_date':str(messages[i].sent_date),
        })
    return json.dumps(data)

# =====================================
