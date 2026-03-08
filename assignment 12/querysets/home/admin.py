from django.contrib import admin
from home.models import Student
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll', 'department', 'pased_in_years', 'pased_out_years']
admin.site.register(Student, StudentAdmin)

