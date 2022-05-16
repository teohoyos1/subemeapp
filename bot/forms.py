from django import forms
from django.contrib.auth.models import User
from .models import bo_bot_tracking

# Create your forms here.
#CREADOTEO
class bot_tracking_form(forms.ModelForm):

    class Meta:
        model = bo_bot_tracking
        fields = ("user","trackingPath", "lastMessage", "phoneMessageFrom",'AccountSid')