from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Profile)
class AdminRegister(admin.ModelAdmin):
    list_display = ['id','user','auth_token','created_at']
