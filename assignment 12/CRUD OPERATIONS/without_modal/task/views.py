from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from task.forms import StudentForm
from task.models import Student

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
    
    
class DeletedView(View):
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        student.delete()
        return redirect('HomeView')