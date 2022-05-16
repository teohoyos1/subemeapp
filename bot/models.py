from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class bo_bot_message(models.Model):
    typeMessage = models.CharField(max_length=70,verbose_name='Tipo de mensaje:')
    message = models.TextField(verbose_name='Mensaje:')
    resume = models.CharField(max_length=70, verbose_name='Abreviatura:',default='test')
    status = models.BooleanField(default=True,verbose_name='Estado:')

    class Meta:
        db_table = 'bo_bot_message'


class bo_bot_tracking(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.RESTRICT)
    trackingPath = models.CharField(max_length=100,blank=True,null=True,default=0)
    lastMessage = models.TextField(blank=True, null=True)
    phoneMessageFrom = models.CharField(max_length=30,blank=True,null=True)
    AccountSid = models.CharField(max_length=100, blank=True, null=True)
    sessionAccount = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        db_table = 'bo_bot_tracking'