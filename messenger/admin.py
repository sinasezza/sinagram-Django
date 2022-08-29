from django.contrib import admin
from . import models


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','user_email','user_phone_number',)

admin.site.register(models.Account,AccountAdmin)
