from django.shortcuts import render
from django.views import View
from django.contrib import messages
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
from config.settings import OPENCAGE_API_KEY
from map.forms import NumberForm
from map.models import Number


class MapView(View):
    def get(self, request):
        return render(request, 'map/map.html', {'form': NumberForm()})

    def post(self, request):
        form = NumberForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            number = form.cleaned_data['number']

            try:
                parsed_number = phonenumbers.parse(number)
            except phonenumbers.NumberParseException:
                messages.error(request, "Invalid phone number format.")
                return render(request, 'map/map.html', context)

            if not phonenumbers.is_valid_number(parsed_number):
                messages.error(request, "Invalid phone number.")
                return render(request, 'map/map.html', context)

            # Save to DB (string format)
            phone_number_obj, created = Number.objects.get_or_create(number=str(parsed_number))

            # Extract info
            location = geocoder.description_for_number(parsed_number, "en") or "Unknown"
            time_zone = ", ".join(timezone.time_zones_for_number(parsed_number)) or "Unknown"
            service_provider = carrier.name_for_number(parsed_number, "en") or "Unknown"

            try:
                geocoder_api = OpenCageGeocode(OPENCAGE_API_KEY)
                results = geocoder_api.geocode(location)
            except Exception as e:
                messages.error(request, f"Geocoding API error: {e}")
                return render(request, 'map/map.html', context)

            if results and len(results):
                latitude = results[0]['geometry']['lat']
                longitude = results[0]['geometry']['lng']
                folium_map = folium.Map(location=[latitude, longitude], zoom_start=9)
                folium.Marker([latitude, longitude], popup=location).add_to(folium_map)

                context['map'] = folium_map._repr_html_()
                context.update({
                    'location': location,
                    'time_zone': time_zone,
                    'service_provider': service_provider,
                })
                messages.success(request, "Phone number information found!")
            else:
                messages.warning(request, "Location info not found.")

        return render(request, 'map/map.html', context)
