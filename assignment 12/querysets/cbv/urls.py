from django.urls import path

from cbv.views import (
    # PersonListView,
    # PersonInheritView
    # PersonTemplateView,
    PersonListView,
    PersonRedirectView
)

urlpatterns = [
    # path('', PersonListView.as_view(), name='person_list'),
    # path('person-inherit/', PersonInheritView.as_view(), name='person_inherit'),
    # path('', PersonTemplateView.as_view(), name='person_template'),
    path('', PersonListView.as_view(), name='person_list'),
    path('', PersonRedirectView.as_view(), name='person_redirect'),
]