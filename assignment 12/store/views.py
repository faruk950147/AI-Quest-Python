from django.shortcuts import render
from django.views import generic

# Create your views here.
class HomeView(generic.View):
    def get(self, request):
        context = {

        }
        return render(request, "store/home.html", context)