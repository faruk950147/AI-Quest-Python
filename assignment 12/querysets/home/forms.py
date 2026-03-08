from django import forms
from .models import Student

class Registration(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'pased_in_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'pased_out_years': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    