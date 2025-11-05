from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from account.forms import SignUpForm, SignInForm, ChangePasswordForm, ResetPasswordForm, SetNewPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
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

class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = SignInForm()
        return render(request, 'account/sign-in.html', {'form': form})

    def post(self, request):
        """ when use authenticationForm use request=request, data=request.POST
        to pass request object and POST data to the form
        when use custom form just pass request.POST
        """
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

class SignOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been signed out successfully.')
        return redirect('sign-in')

class ChangesPasswordView(View):
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'account/change-password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # automatically not log out after password change for 
            # this function update_session_auth_hash optional 
            update_session_auth_hash(request, user)  
            messages.success(request, "Password changed successfully.")
            return redirect('home')  
        else:
            return render(request, 'account/change-password.html', {'form': form})

class ResetPasswordView(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'account/password-reset.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)


                reset_link = request.build_absolute_uri(reverse('password_reset_confirm'))
                messages.success(request, f'Password reset link sent to {email}.')
                
                # send_mail(subject, message, from_email, [email])

                return redirect('password_reset_done')
            else:
                messages.error(request, '।')
        return render(request, 'account/password-reset.html', {'form': form})