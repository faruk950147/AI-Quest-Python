from django.contrib import admin
from queryset.models import Author, Post
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'created_at', 'updated_at']
admin.site.register(Author, AuthorAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
admin.site.register(Post, PostAdmin)



