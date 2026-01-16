from django.contrib import admin
from map.models import Number

class NumberAdmin(admin.ModelAdmin):
    list_display = ['number']
    search_fields = ['number']

admin.site.register(Number, NumberAdmin)
