from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from task.forms import TaskForm

class HomeView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'home.html', {'form': form})
    
    def post(self, request):
        return HttpResponse("POST request")
