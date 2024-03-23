from django.contrib import admin
from . import models

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__','message','sent_date',)


@admin.register(models.PublicRoom)
class PublicRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    

@admin.register(models.PrivateRoom)
class PrivateRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2',)