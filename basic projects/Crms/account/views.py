from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import logout
from account.mixins import LogoutRequiredMixin
from account.utils import account_activation_token
User = get_user_model()
import logging  # noqa: E402
logger = logging.getLogger(__name__)

OTP_EXPIRATION_TIME = 300  # 5 minutes in seconds

# Create your views here.   
@method_decorator(never_cache, name='dispatch')
class ActivationView(generic.View):
    def get(self, request, uidb64, token):
        try:
            # get user id from uidb64
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(get_user_model(), id=user_id)

            # validate the token
            if not account_activation_token.check_token(user, token):
                messages.error(request, 'This token has already been used or is invalid.')
                return redirect('sign')

            # activate the user and login
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('sign')  # Redirect to login page after activation

        except (TypeError, ValueError, OverflowError) as e:
            messages.error(request, 'The activation link is invalid or expired.')
            return redirect('sign')
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
            
@method_decorator(never_cache, name='dispatch')
class SignUpView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/register.html')

    def post(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/register.html')

@method_decorator(never_cache, name='dispatch')
class SignInView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/login.html')

    def post(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/login.html')

@method_decorator(never_cache, name='dispatch')    
class SignOutView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def get(self, request):
        try:
            logout(request)
            messages.success(request, 'You are sign out successfully!')
            return redirect('sign')
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
    
@method_decorator(never_cache, name='dispatch')
class ChangesPasswordView(LoginRequiredMixin, generic.View):
    def get(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/changes-password.html')

    def post(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/changes-password.html')

@method_decorator(never_cache, name='dispatch')    
class SendOTPView(LogoutRequiredMixin, generic.View):
    def post(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/send-otp.html')
    
@method_decorator(never_cache, name='dispatch')    
class ResetPasswordView(LogoutRequiredMixin, generic.View):
    def get(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/reset-password.html')
    
    def post(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/reset-password.html')
        
@method_decorator(never_cache, name='dispatch')    
class ProfileView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def get(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/profile.html')
    def post(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
            return redirect('sign')
        
        return render(request, 'account/profile.html')