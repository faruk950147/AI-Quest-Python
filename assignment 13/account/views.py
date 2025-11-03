from django.shortcuts import render
from django.views import generic
from account.forms import SignUpForm

# Create your views here.

class SignUpView(generic.View):
    def get(self, request):
        context = {
            'form': SignUpForm()
        }
        return render(request, 'account/sign-up.html', context)
    
class SignInView(generic.View):
    def get(self, request):
        return render(request, 'account/sign-in.html')