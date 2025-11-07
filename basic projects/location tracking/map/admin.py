from django.contrib import admin
from map.models import Number
# Register your models here.
class NumberAdmin(admin.ModelAdmin):
    list_display = ['number']
admin.site.register(Number, NumberAdmin)
