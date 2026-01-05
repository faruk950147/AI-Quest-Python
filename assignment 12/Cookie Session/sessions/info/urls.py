from django.urls import path
from info import views

urlpatterns = [
    path('set-session/', views.SetSession.as_view(), name='set-session'),
    path('get-session/', views.GetSession.as_view(), name='get-session'),
]
