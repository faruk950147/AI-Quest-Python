from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, RedirectView
from .models import Person

'''
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

class PersonTemplateView(TemplateView):
    template_name = 'cbv/person_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        return context


'''
class PersonListView(ListView):
    model = Person
    template_name = 'cbv/person_list.html'
    context_object_name = 'persons'

    def get_queryset(self):
        return Person.objects.all()  # Optional because by default it returns all objects


# Redirect View
class PersonRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return '/cbv/person-list/'


   