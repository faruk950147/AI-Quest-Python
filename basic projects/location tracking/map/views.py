from django.shortcuts import render
from django.views import View
from django.contrib import messages
import phonenumbers
import folium
from opencage.geocoder import OpenCageGeocode
from phonenumbers import geocoder, carrier

from config import settings
from map.forms import PhoneSearchForm
from map.models import PhoneSearch  


class MapView(View):
    def get(self, request):
        return render(request, 'map/map.html', {'form': PhoneSearchForm()})

    def post(self, request):
        form = PhoneSearchForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']
            
            # Formatting
            if not str(number).startswith('+'):
                number = "+" + str(number)
            
            try:
                # Parsing
                parsed_number = phonenumbers.parse(number)
                location = geocoder.description_for_number(parsed_number, "en")
                service_provider = carrier.name_for_number(parsed_number, "en")
                
                # Geocoding
                geocoder_api = OpenCageGeocode(settings.OPENCAGE_API_KEY)
                results = geocoder_api.geocode(str(location))
                
                if results:
                    lat = results[0]['geometry']['lat']
                    lng = results[0]['geometry']['lng']

                    # --- DB SAVE OPERATION ---
                    PhoneSearch.objects.create(
                        number=number,
                        location=location,
                        provider=service_provider,
                        latitude=lat,
                        longitude=lng
                    )

                    # Map Generation
                    my_map = folium.Map(location=[lat, lng], zoom_start=9)
                    folium.Marker([lat, lng], popup=f"{location}").add_to(my_map)
                    map_html = my_map._repr_html_()
                    
                    return render(request, 'map/map.html', {
                        'form': form,
                        'map': map_html,
                        'location': location,
                        'provider': service_provider
                    })
                else:
                    messages.error(request, "Could not geocode the location.")
            
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

        return render(request, 'map/map.html', {'form': form})