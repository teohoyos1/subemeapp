from tabnanny import verbose
from django.db import models

# Create your models here.
class Fi_file_type(models.Model):
    name = models.TextField() #foruser
    parentID = models.IntegerField(blank=True,default=0) #interno if foruser
    isActive = models.IntegerField(default=0) #interno

    class Meta:
        unique_together = ('name',)
        # verbose_name = 'File_type'
        # verbose_name_plural = 'File_types'
        # db_table = 'fi_File_type'
        # ordering = ['name','parentID','isActive']


class Fi_file(models.Model):
    fileType = models.ForeignKey(Fi_file_type, null=True, blank=True, on_delete=models.CASCADE)
    fileDescription = models.TextField(max_length=250) #foruser
    filePath = models.FileField(null=True, blank=True) #interno JSON and foruser
    fileDate = models.DateField(auto_now=True) #interno