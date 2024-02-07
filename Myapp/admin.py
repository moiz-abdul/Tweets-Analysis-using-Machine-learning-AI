from django.contrib import admin
from .models import Uzerlogin,PasswordResetOTP,UserMessage

# Register your models here.

admin.site.register(Uzerlogin)
admin.site.register(PasswordResetOTP)
admin.site.register(UserMessage)
