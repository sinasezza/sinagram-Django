from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('get-or-create-room/<str:receiver_id>/', views.get_or_create_room, name='get-or-create-room'),
    path('contact-chat/<str:room_id>/',views.contact_chat_view,name='contact-chat'),
    path('contact/<int:id>/message-count/',views.get_message_numbers,name='message_count'),
    path('contact/<int:id>/get-all-messages/',views.get_all_messages,name='get_all_messages'),
    path('delete-message/<int:id>/',views.delete_message,name='delete_message'),
]