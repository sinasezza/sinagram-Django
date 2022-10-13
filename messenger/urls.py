from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('',views.main_page,name='main_page'),
    path('Signup/',views.signup_view,name='signup'),
    path('Login/',views.login_view,name='login'),
    path('Logout/',views.Logout_view,name='logout'),
    path('panel/<str:username>',views.panel_view,name='panel'),
    path('panel/<str:username>/change-info/',views.change_account_info_view,name='change_account_info'),
    path('panel/<str:username>/delete-user/',views.delete_user_view,name='delete_user'),
    path('<str:username>/contact-list/',views.contact_list_view,name='contacts'),
    path('<str:username>/add-contact/',view=views.add_contact_view,name='add_contact'),
    path('<str:username>/contact/<str:name>-<int:id>/',view=views.contact_detail_view,name='contact_detail'),
    path('<str:username>/contact/<str:name>-<int:id>/change-info',view=views.change_contact_info_view,name='change_contact_info'),
    path('<str:username>/contact/<str:name>-<int:id>/delete-contact',views.delete_contact_view,name='delete_contact'),
    path('contact/<int:id>/',views.contact_chat_view,name='contact_chat'),
    path('contact/<int:id>/message-count/',views.get_message_numbers,name='message_count'),
    path('contact/<int:id>/get-all-messages/',views.get_all_messages,name='get_all_messages'),
    path('delete-message/<int:id>/',views.delete_message,name='delete_message'),
    path('edit-message/<int:id>/',views.edit_message_view,name='edit_message'),
    # path('edit')




]