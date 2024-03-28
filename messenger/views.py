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
from users import decorators as users_decorators
from users import models as users_models
from . import models,forms



# ======================================

@login_required(login_url='messenger:login')
@users_decorators.profile_required
def contact_chat_view(request, id: str):
    print(f'id is {id}')
    sender = request.user.profile
    receiver = get_object_or_404(users_models.UserProfile, id=id)
    form = forms.SendMessageForm()
    
    context = {
        'form': form,
        'sender': sender,
        'receiver': receiver,
    }
    return render(request, 'messenger/contact_chat_page.html', context)

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

def make_data_message(messages):
    data = []
    for i in range(len(messages)):
        if(messages[i].content != 'False'):
            data.append({
                'id':messages[i].id,
                'sender':messages[i].sender.user.username,
                'message':messages[i].message,
                'file':'/media/'+str(messages[i].content),
                'sent_date':str(messages[i].sent_date),
            })
        else:  
            data.append({
                'id':messages[i].id,
                'sender':messages[i].sender.user.username,
                'message':messages[i].message,
                'file':str(messages[i].content),
                'sent_date':str(messages[i].sent_date),
            })
    return json.dumps(data)

# =====================================
