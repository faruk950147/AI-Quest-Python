from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import generic
from django.contrib.auth.models import User
from account.forms import (
    SignUpForm,
    SignInForm,
    ChangePasswordForm,
)

# Create your views here.
class SignUpView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        form = SignUpForm()
        return render(request, 'account/sign-up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('sign-in')
        messages.error(request, 'Please correct the errors below.')
        return render(request, 'account/sign-up.html', {'form': form})

""" class SignInView(generic.View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        form = SignInForm()
        return render(request, 'account/sign-in.html', {'form': form})

    def post(self, request):
        # when use authenticationForm use request=request, data=request.POST
        # to pass request object and POST data to the form
        # when use custom form just pass request.POST
        
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'account/sign-in.html', {'form': form})

class SignOutView(generic.View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('sign-in')
     """
class PasswordChangeView(generic.View):
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'account/password-change.html', {'form': form})
    
class PasswordResetView(generic.View):
    def get(self, request):
        return render(request, 'account/password-reset.html', {})

class ProfileView(generic.View):
    def get(self, request):
        return render(request, 'account/profile.html', {})
