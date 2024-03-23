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

from . import models,forms



# ======================================

@login_required(login_url= 'messenger:login')
def contact_chat_view(request,id):
    sender = models.Account.objects.get(id__exact = request.user.id)
    receiver = models.Account.objects.get(id__exact = id)

    if request.method == 'POST':
        form = forms.SendMessageForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            message = models.Message.objects.create(  sender=sender ,
                                            receiver=receiver,
                                            message=cd['message'],
                                            content=request.FILES.get('file',False))
            message.save()
            return JsonResponse(make_data_message([message,]),safe=False)
        else:
            messages.error(request,'form is not valid')

    else :
            form = forms.SendMessageForm()
            form.fields['sender_id'].initial = sender.id
            form.fields['receiver_id'].initial = receiver.id
            return render(request,'messenger_pages/contact_chat_page.html',context={'form':form,})

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
