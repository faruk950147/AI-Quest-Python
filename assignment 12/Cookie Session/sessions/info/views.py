from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse


class SetSession(generic.View):
    def get(self, request, *args, **kwargs):
        request.session['user_name'] = 'Faruk Cse'
        request.session['user_id'] = 123
        return HttpResponse('Session set successfully')
    
    
class GetSession(generic.View):
    def get(self, request, *args, **kwargs):
        user_name = request.session.get('user_name', 'Guest')
        user_id = request.session.get('user_id', None)
        return HttpResponse(f'User: {user_name}, ID: {user_id}')
    
