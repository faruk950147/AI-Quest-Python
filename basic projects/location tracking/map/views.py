from django.shortcuts import render
from django.views import View
from django.contrib import messages
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
from django.conf import settings
from map.forms import NumberForm
from map.models import Number

class MapView(View):
    def get(self, request):
        return render(request, 'map/map.html', {'form': NumberForm()})

    def post(self, request):
        form = NumberForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']

            print(f"========== Received number ==========: {number}")

        return render(request, 'map/map.html', {'form': form})
