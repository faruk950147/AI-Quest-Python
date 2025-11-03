from django.shortcuts import render
from django.views import generic

# Create your views here.

class SignUpView(generic.View):
    def get(self, request):
        return render(request, 'account/sign-up.html')
    
class SignInView(generic.View):
    def get(self, request):
        return render(request, 'account/sign-in.html')