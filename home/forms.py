from django import forms
from .models import Content

class AddForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'
