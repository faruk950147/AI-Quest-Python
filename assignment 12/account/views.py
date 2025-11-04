from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import generic
from account.forms import SignUpForm, SignInForm
# Create your views here.
class SignUpView(generic.View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'account/sign-up.html', {'form': form})
    
class SignInView(generic.View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'account/sign-in.html', {'form': form})

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
