from django.shortcuts import render
from django.views import generic

# Create your views here.
class CollageView(generic.View):
    def get(self, request):
        context = {
            
        }
        return render(request, "collage/collage.html", context)
