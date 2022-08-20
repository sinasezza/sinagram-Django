from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('',views.main_page,name='main_page'),
    path('Signup',views.signup_view,name='signup'),
    path('Login',views.login_view,name='login'),
    path('Logout',views.Logout_view,name='logout'),
    
]