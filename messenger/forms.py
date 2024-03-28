from django import forms
from . import models

class SendMessageForm(forms.ModelForm):
    
    sender_id   = forms.IntegerField(label='sender_id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)
    # -----------------------------------
    receiver_id = forms.IntegerField(label='receiver_id',widget=forms.HiddenInput(attrs={'readonly':True,}),required=False)
    # -----------------------------------
    file        = forms.FileField(label='file',required=False)
    # -----------------------------------
    message     = forms.CharField(label='message',required=False,max_length=500,widget=forms.Textarea(attrs={'autofocus':True,'rows':2,'cols':70,'id':'id_text','style':'resize:none;',}))

    class Meta:
        model   = models.Message
        fields = ('message',)