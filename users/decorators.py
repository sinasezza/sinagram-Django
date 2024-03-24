from django.shortcuts import redirect
from django.contrib import messages
from . import models


def logout_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request,'you are already logged in , please log out and try again')
            return redirect('generics:main-page')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def profile_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not models.UserProfile.objects.filter(user=request.user).exists():
                messages.warning(request, 'you should complete you profile info!')
                return redirect('users:create-profile')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view