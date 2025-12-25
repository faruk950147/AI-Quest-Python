from django.shortcuts import render
from django.views import generic
# Create your views here.

class InfoView(generic.View):
    template_name = 'info/info.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
        
        })

class InfoDetailView(generic.View):
    template_name = 'info/info-detail.html'

    def get(self, request, *args, **kwargs):
        info_id = kwargs.get('id')
        return render(request, self.template_name, {
            'info_id': info_id
        })
