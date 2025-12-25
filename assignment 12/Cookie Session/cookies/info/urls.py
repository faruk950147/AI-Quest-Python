from django.urls import path
from info import views
urlpatterns = [
    path('', views.InfoView.as_view(), name='home'),
    path('info/<int:id>/', views.InfoDetailView.as_view(), name='info'),
]