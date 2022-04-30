from django.contrib import admin
from .models import Fi_file_type
# Register your models here.

class Fi_file_type_Admin(admin.ModelAdmin):
    list_display = ['id', 'name','isActive']

admin.site.register(Fi_file_type, Fi_file_type_Admin)
