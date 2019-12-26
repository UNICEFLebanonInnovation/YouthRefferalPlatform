from django.conf.urls import url
from . import views
from .autocompletes import LocationAutocomplete



urlpatterns = [
    url(r'^location-autocomplete/$',
        LocationAutocomplete.as_view(),
        name='location-autocomplete',
        ),

    url(
        regex=r'^exec-sequence/$',
        view=views.ExecSequenceView.as_view(),
        name='exec_sequence'
    ),
]
