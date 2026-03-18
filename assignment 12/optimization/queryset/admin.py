from django.contrib import admin
from queryset.models import Author, Tag, Post
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'created_at', 'updated_at']
admin.site.register(Author, AuthorAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(Tag, TagAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
admin.site.register(Post, PostAdmin)



