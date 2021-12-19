from .models import ProblemRequest
from django import forms
from django.core.validators import validate_slug

class ProblemRequestForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder': 'Ваше имя..', 'style':'margin-bottom:15px;'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '10', 'placeholder': 'Описание..', 'style':'margin-bottom:15px;'}
    ))
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = ProblemRequest

        fields = {'name', 'description', 'image'}