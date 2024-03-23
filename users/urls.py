from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.Logout_view, name='logout'),
    path('create-profile/', views.create_profile_view, name='create-profile'),
]
