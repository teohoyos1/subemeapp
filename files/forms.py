from django import forms
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import boto3
#from django.forms import ClearableFileInput
from .models import Fi_file_type, Fi_file

class Fi_file_typeForm(forms.ModelForm):
    class Meta:
        model = Fi_file_type
        fields = ['name','isActive']


class Fi_fileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        userReq = kwargs.pop('user')
        super(Fi_fileForm, self).__init__(*args, **kwargs)
        self.fields['fileType'] = forms.ModelChoiceField(queryset=Fi_file_type.objects.filter(isActive=1, user=userReq),empty_label="Seleccione...", label="Grupo:")

    class Meta:
        model = Fi_file
        fields = ['fileType','fileTypeName','fileDescription','files']
        # widgets = {
        #     'media': ClearableFileInput(attrs={'multiple': True})
        # }

class Fi_fileFormEditWOFile(forms.ModelForm):
    class Meta:
        model = Fi_file
        fields = ['fileTypeName','fileDescription']

class Fi_fileFormEditWithFile(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self._pwd = kwargs.pop('pwd', None)
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = Fi_file
        fields = ['fileTypeName','fileDescription','files']


    def save(self, *args, **kwargs):
        try:
            this = Fi_file.objects.get(id=self.instance.id)
            if this.files:
                if str(os.getenv('USE_S3_CLOUD'))=="1":
                    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                    path = os.path.join(settings.MEDIA_ROOT, this.files.name)
                    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=path)
                else:
                    path ="."+this.files.url
                    os.remove(path)
        except ObjectDoesNotExist:
            pass
        super(Fi_fileFormEditWithFile, self).save(*args, **kwargs)