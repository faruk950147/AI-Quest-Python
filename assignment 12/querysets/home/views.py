from django.shortcuts import render
from django.views import generic
from home.forms import Registration
from home.models import Student

class StudentRegistrationPost(generic.View):

    def get(self, request):
        context = {'form': Registration(), 'students': Student.objects.all()}
        return render(request, 'home.html', context)

    def post(self, request):
        form = Registration(request.POST)

        if form.is_valid():
            form.save()
            form = Registration()

        context = {'form': form}
        return render(request, 'home.html', context)