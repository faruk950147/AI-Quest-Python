from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
    PasswordChangeForm, #it's with old password
    SetPasswordForm  #it's without old password
)

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
    
    class Meta:
        model = User
        fields = ['username', 'password']

class ChangePasswordForm(PasswordChangeForm):
    # Extending the parent class PasswordChangeForm
    def __init__(self, user, *args, **kwargs):
        # Call the parent class __init__ method
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs) 
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs) 
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter old password', 'type': 'password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter new password', 'type': 'password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm new password', 'type': 'password'})

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
