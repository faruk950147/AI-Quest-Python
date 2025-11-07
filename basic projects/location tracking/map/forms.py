from django import forms
from map.models import Number

class NumberForm(forms.ModelForm):
    class Meta:
        model = Number
        fields = ['number']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your number', 'id': 'number'}),
        }
