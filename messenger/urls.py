from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('',views.main_page,name='main_page'),
    path('Signup/',views.signup_view,name='signup'),
    path('Login/',views.login_view,name='login'),
    path('Logout/',views.Logout_view,name='logout'),
    path('panel/<str:username>',views.panel_view,name='panel'),
    path('panel/<str:username>/change_info/',views.change_info_view,name='change_info'),
    path('panel/<str:username>/delete_user/',views.delete_user_view,name='delete_user'),
    
]