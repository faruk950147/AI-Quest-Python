from django import forms
class Registration(forms.Form):
    name = forms.CharField()
    roll = forms.IntegerField()
    department = forms.CharField()






class Registration(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    roll = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    department = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    