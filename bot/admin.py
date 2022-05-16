from django.contrib import admin
from .models import bo_bot_message,bo_bot_tracking
# Register your models here.
class bo_bot_message_Admin(admin.ModelAdmin):
    list_display = ['id', 'typeMessage','message','resume','status']

class bo_bot_tracking_Admin(admin.ModelAdmin):
    list_display = ['id', 'user','trackingPath','lastMessage','phoneMessageFrom','AccountSid','sessionAccount']


admin.site.register(bo_bot_message, bo_bot_message_Admin)
admin.site.register(bo_bot_tracking, bo_bot_tracking_Admin)