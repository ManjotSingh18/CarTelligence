from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    pic = forms.ImageField(label='', required=False)
    class Meta:
        model= Car
        fields=['pic']
    
