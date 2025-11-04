from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import generic
from accounts.forms import SignUpForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash

# Sign-up View
class SignUpView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = SignUpForm()
        return render(request, 'accounts/sign-up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('sign-in')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'account/sign-up.html', {'form': form})

# Password Change View
class PasswordChangeView(generic.View):
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'accounts/password-change.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevent logout after password change
            messages.success(request, 'Password changed successfully.')
            return redirect('home')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'accounts/password-change.html', {'form': form})

# Password Reset View
class PasswordResetView(generic.View):
    def get(self, request):
        return render(request, 'accounts/password-reset.html', {})

# Profile View
class ProfileView(generic.View):
    def get(self, request):
        return render(request, 'accounts/profile.html', {})
