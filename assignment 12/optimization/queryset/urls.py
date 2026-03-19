from django.urls import path
from queryset.views import (
    PostListWithoutSelectRelatedView,
    PostListWithSelectRelatedView,
    PostListWithoutPrefetchRelatedView,
    PostListWithPrefetchRelatedView,
    PostListOptimizedView,
)

urlpatterns = [
    path('posts/no-select/', PostListWithoutSelectRelatedView.as_view(), name='posts-no-select'),
    path('posts/select/', PostListWithSelectRelatedView.as_view(), name='posts-select'),
    path('posts/no-prefetch/', PostListWithoutPrefetchRelatedView.as_view(), name='posts-no-prefetch'),
    path('posts/prefetch/', PostListWithPrefetchRelatedView.as_view(), name='posts-prefetch'),
    path('posts/optimized/', PostListOptimizedView.as_view(), name='posts-optimized'),
]