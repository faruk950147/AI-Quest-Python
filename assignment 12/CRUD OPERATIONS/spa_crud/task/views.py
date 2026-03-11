from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import F

from task.models import Task
from task.forms import TaskForm


class HomeView(View):
    def get(self, request):
        tasks = Task.objects.all()
        form = TaskForm()
        return render(request, 'home.html', {'form': form, 'tasks': tasks})
    
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.is_completed = False
            task.save()
            return JsonResponse({
                'success': True,
                'task': {
                    'id': task.id,
                    'name': task.name,
                    'department': task.department,
                    'phone': task.phone,
                    'is_completed': task.is_completed
                }
            })
        return JsonResponse({'success': False, 'errors': form.errors})


class ToggleTaskView(View):
    def post(self, request):
        pk = request.POST.get('pk')
        task_qs = Task.objects.filter(pk=pk)
        if task_qs.exists():
            task_qs.update(is_completed=~F('is_completed'))
            task = task_qs.first()
            return JsonResponse({
                'id': task.id,
                'is_completed': task.is_completed
            })
        return JsonResponse({'error': 'Task not found'}, status=404)