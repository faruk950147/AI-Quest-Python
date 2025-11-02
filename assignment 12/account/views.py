from django.shortcuts import render, redirect
from django.views import generic
# Create your views here.
class SignUpView(generic.View):
    def get(self, request):
        
        return render(request, 'account/sign-up.html', {})
    
class SignInView(generic.View):
    def get(self, request):
        return render(request, 'account/sign-in.html', {})

class SignOutView(generic.View):
    def get(self, request):
        return redirect('sign-in')
    
class PasswordChangeView(generic.View):
    def get(self, request):
        return render(request, 'account/password-change.html', {})
    
class PasswordResetView(generic.View):
    def get(self, request):
        return render(request, 'account/password-reset.html', {})

class ProfileView(generic.View):
    def get(self, request):
        return render(request, 'account/profile.html', {})
