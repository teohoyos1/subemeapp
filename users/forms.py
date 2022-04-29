from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your forms here.
#CREADOTEO
class CustomNewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

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
