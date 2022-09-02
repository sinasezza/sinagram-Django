from django.contrib import admin
from . import models


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user','user_email','user_phone_number',)


# ======================================
# ======================================

class ContactAdmin(admin.ModelAdmin):
    list_display = ('username','fname','lname','phone_number','email')


# ======================================
# ======================================


admin.site.register(models.Account,AccountAdmin)
admin.site.register(models.Contact,ContactAdmin)
