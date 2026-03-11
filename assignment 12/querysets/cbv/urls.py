from django.urls import path

from cbv.views import (
    PersonListView
)

urlpatterns = [
    path('', PersonListView.as_view(), name='person_list'),
]