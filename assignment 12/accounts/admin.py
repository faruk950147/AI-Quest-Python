from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    # readonly_fields = ('username', 'email', 'first_name', 'password', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

# unregister default User admin
admin.site.unregister(User)
# register custom User admin
admin.site.register(User, UserAdmin)
