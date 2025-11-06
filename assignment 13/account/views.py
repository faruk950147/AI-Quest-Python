from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
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

                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )

                # Send email (update subject & message as needed)
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link below to reset your password:\n{reset_link}',
                    from_email='no-reply@example.com',
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, f'Password reset link has been sent to {email}.')
                return redirect('sign-in')
            else:
                messages.error(request, 'No user is associated with this email.')
        return render(request, 'account/password-reset.html', {'form': form})

class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if user is not None and default_token_generator.check_token(user, token):
            form = SetNewPasswordForm(user)
            return render(request, 'account/set-new-password.html', {'form': form, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('reset-password')

    def post(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if user is not None and default_token_generator.check_token(user, token):
            form = SetNewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password has been reset successfully. You can now sign in.')
                return redirect('sign-in')
            return render(request, 'account/set-new-password.html', {'form': form, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('reset-password')
