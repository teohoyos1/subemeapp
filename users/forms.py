from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Person

# Create your forms here.
#CREADOTEO
class CustomNewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username","email", "password1", "password2")

    # def save(self, commit=True):
    #     user = super(CustomNewUserForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user


class ProfileForm(UserChangeForm):
    password = None
    #overwrite
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
        labels = {
            "first_name": _("Nombre:"),
            "last_name": _("Apellidos:"),
            "email": _("Email:")
        }

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('phone_number','address')
        unique_together = ('phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'id': 'phone'})
