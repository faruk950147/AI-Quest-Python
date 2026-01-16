from django import forms
from map.models import Number
import phonenumbers
from django.core.exceptions import ValidationError

class NumberForm(forms.ModelForm):
    class Meta:
        model = Number
        fields = ['number']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'id': 'number'
            }),
        }