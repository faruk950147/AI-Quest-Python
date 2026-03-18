from django.urls import path
from queryset.views import PostListView
urlpatterns = [
    path('', PostListView.as_view(), name = 'PostListView'),
]
