from pyexpat import model
from django import forms
from .models import Fi_file_type

class Fi_file_typeForm(forms.ModelForm):
    class Meta:
        model = Fi_file_type
        fields = ['name','parentID','isActive']
        exclude = ['parentID']


    def clean(self):
        data = self.cleaned_data
        name = data.get('name')
        qs = Fi_file_type.objects.filter(name__icontains=name)
        if qs.exists():
            self.add_error('name',f'El nombre del grupo {name} ya se encuentra creado.')
        return data
