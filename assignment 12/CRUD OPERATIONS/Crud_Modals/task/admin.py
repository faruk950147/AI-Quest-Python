from django.contrib import admin
from task.models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'department', 'phone'
    ]
admin.site.register(Student, StudentAdmin)