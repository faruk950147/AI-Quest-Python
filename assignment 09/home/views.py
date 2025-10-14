from django.shortcuts import render
from django.views import generic
from home.forms import Registration
# Create your views here.
class HomeView(generic.View):
    def get(self, request):
        
        return render(request, 'home/home.html')
    
    
class RegistrationView(generic.View):
    def get(self, request):
        form = Registration(auto_id='id_%s') # Custom auto_id prefix for form fields id customization
        return render(request, 'home/registration.html', {'form': form})
    
    def post(self, request):
        form = Registration(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            roll = form.cleaned_data['roll']
            department = form.cleaned_data['department']
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']
            agree = form.cleaned_data['agree']
            context = {
                'name': name,
                'roll': roll,
                'department': department,
                'email': email,
                'dob': dob,
                'agree': agree
            }
            return render(request, 'home/success.html', context)
        return render(request, 'home/registration.html', {'form': form})
