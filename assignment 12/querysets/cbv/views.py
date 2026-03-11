from django.shortcuts import render
from django.views import View
from .models import Person


class PersonListView(View):
    def get(self, request):
        persons = Person.objects.all()
        return render(request, 'cbv/person_list.html', {'persons': persons})

    def post(self, request):
        
        return render(request, 'cbv/person_list.html', {'persons': persons})


# Inherit View
class PersonInheritView(PersonListView):
    def get(self, request):
        # call the super method
        return super().get(request)
        

    def post(self, request):
        # call the super method
        return super().post(request)
        