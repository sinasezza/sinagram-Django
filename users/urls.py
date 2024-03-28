from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.Logout_view, name='logout'),
    path('create-profile/', views.create_profile_view, name='create-profile'),
    path('panel/', views.panel_view, name='my-panel'),
    path('panel/<str:username>/', views.panel_view, name='panel'),
    path('panel-edit/', views.change_account_info_view, name='panel-edit'),
    path('panel/delete/', views.delete_user_view, name='panel-delete'),
    path('contacts/', views.contact_list_view, name='contact-list'),
    path('contacts/<int:id>/', views.contact_detail_view, name='contact-detail'),
    path('contacts/add/', views.add_contact_view, name='add-contact'),
]
