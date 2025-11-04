from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
    PasswordResetForm
)

# ------------------ Sign Up Form ------------------
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter email')})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter username')})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter password')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm password')})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Username already exists"))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email already exists"))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# ------------------ Sign In Form ------------------
class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter username')})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter password')})


# ------------------ Change Password Form ------------------
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter old password'), 'type': 'password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter new password'), 'type': 'password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm new password'), 'type': 'password'})


# ------------------ Reset Password Form ------------------
class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter your registered email')})


# ------------------ Set New Password Form ------------------
class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Enter new password'), 'type': 'password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirm new password'), 'type': 'password'})
