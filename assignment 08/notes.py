# import uuid
# from django.db import models
# from django.shortcuts import render
# from django.views.generic import DetailView, RedirectView, View
# from .models import Note
# from uuid import UUID

# class Note(models.Model):
#     id = models.AutoField(primary_key=True)
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     slug = models.SlugField(unique=True)
#     title = models.CharField(max_length=200)
#     content = models.TextField()

#     class Meta:
#         ordering = ['title']

#     def __str__(self):
#         return self.title


# Index View
# class IndexView(View):
#     def get(self, request):
#         notes = Note.objects.all()
#         return render(request, 'index.html', {'notes': notes})


# Detail by ID
# class NoteDetailByIdView(DetailView):
#     model = Note
#     template_name = 'note_detail.html'
#     context_object_name = 'note'
#     pk_url_kwarg = 'note_id'


# Detail by Slug
# class NoteDetailBySlugView(DetailView):
#     model = Note
#     template_name = 'note_detail.html'
#     context_object_name = 'note'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'


# Detail by UUID
# class NoteDetailByUUIDView(DetailView):
#     model = Note
#     template_name = 'note_detail.html'
#     context_object_name = 'note'
#     pk_url_kwarg = 'note_id'

#     def get_object(self, queryset=None):
#         note_id = self.kwargs.get('note_id')
#         return Note.objects.get(uuid=UUID(str(note_id)))


#  Redirect View
# class NoteRedirectView(RedirectView):
#     url = '/'  # Redirect to homepage
    
    
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('note/id/<int:note_id>/', views.NoteDetailByIdView.as_view(), name='note_detail_by_id'),
#     path('note/slug/<str:slug>/', views.NoteDetailBySlugView.as_view(), name='note_detail_by_slug'),
#     path('note/uuid/<uuid:note_id>/', views.NoteDetailByUUIDView.as_view(), name='note_detail_by_uuid'),
#     path('note/redirect/', views.NoteRedirectView.as_view(url='/'), name='note_redirect'),
# ]


# <!DOCTYPE html>
# <html>
# <head>
#     <title>Notes Index</title>
# </head>
# <body>
#     <h1>All Notes</h1>
#     <ul>
#         {% for note in notes %}
#             <li>
#                 <strong>{{ note.title }}</strong><br>
#                 <a href="{% url 'note_detail_by_id' note.id %}">By ID</a> |
#                 <a href="{% url 'note_detail_by_slug' note.slug %}">By Slug</a> |
#                 <a href="{% url 'note_detail_by_uuid' note.uuid %}">By UUID</a>
#             </li>
#         {% empty %}
#             <li>No notes available.</li>
#         {% endfor %}
#     </ul>

#     <a href="{% url 'note_redirect' %}">Go to Redirect View</a>
# </body>
# </html>
