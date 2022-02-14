from django import forms
from .models import todo

class todoform(forms.ModelForm):
    class Meta:
        model = todo
        exclude = ['user']