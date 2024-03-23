from django.shortcuts import redirect
from django.contrib import messages


def logout_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request,'you are already logged in , please log out and try again')
            return redirect('generics:main-page')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view