from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse    
from django.shortcuts import render, redirect

User = get_user_model()
import logging
logger = logging.getLogger(__name__)

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class TasksView(generic.View):
    def get(self, request):
        try:
            pass
        except Exception as e:
            logger.error(f"{e}")
        return render(request, 'tasks/tasks.html')