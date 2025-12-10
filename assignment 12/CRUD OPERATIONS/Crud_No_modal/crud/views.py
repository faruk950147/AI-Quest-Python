from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from crud.forms import StudentForm
from crud.models import Student

class HomeView(View):
    def get(self, request):
        students = Student.objects.all()
        form = StudentForm()
        return render(request, 'home.html', {'students': students, 'form': form})

class SavedView(View):
    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('HomeView')
"""
# extra edit.html page
class EditedView(View):
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        form = StudentForm(instance=student)
        return render(request, 'edit.html', {'form': form, 'student': student})

    def post(self, request, id):
        student = get_object_or_404(Student, id=id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('HomeView')
        return render(request, 'edit.html', {'form': form, 'student': student})
        
# Single page create and Edit and Delete View 

class EditedView(View):
    def post(self, request, id):
        student = get_object_or_404(Student, id=id)
        name = request.POST.get('name')
        department = request.POST.get('department')
        phone = request.POST.get('phone')
        if name or department or phone:
            student.name = name
            student.department = department
            student.phone = phone
            student.save()
            return redirect('HomeView')
        else:
            return redirect('HomeView')


"""
class EditedView(View):
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        form = StudentForm(instance=student)
        return render(request, 'edit.html', {'form': form, 'student': student})
    
    def post(self, request, id):
        student = get_object_or_404(Student, id=id)
        name = request.POST.get('name')
        department = request.POST.get('department')
        phone = request.POST.get('phone')
        if name or department or phone:
            student.name = name
            student.department = department
            student.phone = phone
            student.save()
            return redirect('HomeView')
        else:
            return redirect('HomeView')


class DeletedView(View):
    def post(self, request, id):
        student = get_object_or_404(Student, id=id)
        student.delete()
        return redirect('HomeView')
