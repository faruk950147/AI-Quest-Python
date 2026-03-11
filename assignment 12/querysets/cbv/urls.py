from django.urls import path

from cbv.views import (
    PersonListView,
    PersonInheritView
)

urlpatterns = [
    path('', PersonListView.as_view(), name='person_list'),
    path('person-inherit/', PersonInheritView.as_view(), name='person_inherit'),
]