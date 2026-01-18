from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from task.forms import TaskForm
from task.models import Task

class HomeView(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'home.html', {'tasks': tasks})

    def post(self, request):
        # Add new task
        name = request.POST.get('name')
        department = request.POST.get('department')
        phone = request.POST.get('phone')

        if name and department and phone:
            Task.objects.create(name=name, department=department, phone=phone)
        
        return redirect('HomeView')


class EditedView(View):
    def post(self, request, id):
        # Edit existing task
        task = get_object_or_404(Task, id=id)
        # form = TaskForm(request.POST, instance=task)
        name = request.POST.get('name')
        department = request.POST.get('department')
        phone = request.POST.get('phone')

        if name and department and phone:
            task.name = name
            task.department = department
            task.phone = phone
            task.save()

        return redirect('HomeView')


class DeletedView(View):
    def get(self, request, id):
        # Delete task
        task = get_object_or_404(Task, id=id)
        task.delete()
        return redirect('HomeView')
