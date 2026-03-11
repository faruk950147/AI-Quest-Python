from django.urls import path

from cbv.views import (
    ShowView
)

urlpatterns = [
    path('', ShowView.as_view(), name='show'),
]