from django.shortcuts import render, redirect
from django.views import View
from home.forms import Registration
from home.models import Student

class StudentRegistrationPost(View):

    def get(self, request):
        form = Registration()
        # Get all students
        # students = Student.objects.all()
        # Get students with department 'BBA'
        # students = Student.objects.filter(department='BBA')
        # Get students with department 'BBA' and age greater than 20
        students = Student.objects.filter(department='BBA', age__gt=20)
        return render(request, 'home.html', {'form': form, 'students': students})

    def post(self, request):
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('StudentRegistrationPost')
        students = Student.objects.all()
        return render(request, 'home.html', {'form': form, 'students': students})