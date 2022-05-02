from django.contrib import admin
from .models import Fi_file_type,Fi_file
# Register your models here.

class Fi_file_type_Admin(admin.ModelAdmin):
    list_display = ['id', 'name','isActive']

class Fi_file_Admin(admin.ModelAdmin):
    list_display = ['id', 'fileType','fileTypeName','fileDescription','files','modified_date']

admin.site.register(Fi_file_type, Fi_file_type_Admin)
admin.site.register(Fi_file, Fi_file_Admin)
