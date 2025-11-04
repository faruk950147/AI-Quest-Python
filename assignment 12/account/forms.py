from django import forms
from django.contrib.auth.models import User
# why use gettext_lazy as _ ? because it's for translation purpose
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    PasswordChangeForm,  # it's with old password
    SetPasswordForm      # it's without old password
)
class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    