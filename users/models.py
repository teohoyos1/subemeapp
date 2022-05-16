from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100,verbose_name='Teléfono:',blank=True,null=True)
    address = models.CharField(max_length=100, verbose_name='Dirección:', help_text='Ingrese la dirección',blank=True,null=True)

    class Meta:
        unique_together = ('phone_number',)