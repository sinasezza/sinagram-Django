from django.shortcuts import render , redirect , HttpResponse , HttpResponseRedirect
from django.contrib.auth.models import User 
from django.contrib.auth import login , get_user_model , authenticate , logout
from django.contrib import messages
from . import models,forms



def main_page(request):
    return render(request , 'Home/main_page.html')

# ======================================

def signup_view(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password1'] != cd['password2']:
                return HttpResponseRedirect('accounts:signup','passwords are not same')
            newUser = User( username=cd['username'],
                            first_name=cd['first_name'],
                            last_name=cd['last_name'],
                            email=cd['email'])
            newUser.set_password(cd['password1'])
            newUser.save()
            newAccount =  models.Account(   user=newUser,
                                            user_age=cd['age'],
                                            user_phone_number=cd['phone_number'],)
            newAccount.save()
            return redirect('messenger:main_page')
        else:
            print(form.errors.as_data())
            return HttpResponse('form is not valid')
        
    else:
        form = forms.SignupForm()

    content = {
        'form' : form,
    }

    return render(request,'forms/signup_page.html',content)

# ======================================

def login_view(request):
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

def Logout_view(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('messenger:main_page')