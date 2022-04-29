from django.db import models

# Create your models here.
# class Fi_File(models.Model):
#     fileTypeId = models.ForeignKey('Fi_file_type', on_delete=models.CASCADE,)
#     fileName = models.TextField(max_length=250) #interno
#     fileDescription = models.TextField(max_length=250) #foruser
#     filePath = models.TextField(max_length=250) #interno JSON and foruser
#     fileDate = models.DateField(auto_now=True) #interno

class Fi_file_type(models.Model):
    name = models.TextField() #foruser
    parentID = models.IntegerField(blank=True,default=0) #interno if foruser
    isActive = models.IntegerField(default=0) #interno

    class Meta:
        unique_together = ('name',)