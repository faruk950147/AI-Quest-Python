from django.shortcuts import render
from django.views import View
from cbv.models import Person

# Create your views here.
class PersonListView(View):
    def get(self, request):
        persons = Person.objects.all()
        return render(request, 'cbv/person_list.html', {'persons': persons})
    def post(self, request):
        pass

