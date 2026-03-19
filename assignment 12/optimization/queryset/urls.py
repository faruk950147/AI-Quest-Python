from django.urls import path
from queryset.views import PostListView, PostListViewOptimazed

urlpatterns = [
    path('', PostListView.as_view(), name = 'PostListView'),
    path('optimazed/', PostListViewOptimazed.as_view(), name = 'PostListViewOptimazed'),
]
