from django.urls import path
from info import views
urlpatterns = [
    path('', views.InfoView.as_view(), name='info'),
    path('info-detail/<int:id>/', views.InfoDetailView.as_view(), name='info-detail'),
]