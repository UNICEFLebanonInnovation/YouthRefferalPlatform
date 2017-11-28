from django.utils.translation import ugettext as _

from django_filters import FilterSet, ModelChoiceFilter

from referral_platform.locations.models import Location
from .models import YoungPerson, Nationality


class CommonFilter(FilterSet):
    governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__isnull=False), empty_label=_('Governorate'))
    nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))


class YouthFilter(CommonFilter):

    class Meta:
        model = YoungPerson
        fields = {
            'bayanati_ID': ['contains'],
            'location': ['contains'],
            'trainer': ['contains'],
            'first_name': ['contains'],
            'father_name': ['contains'],
            'last_name': ['contains'],
            'nationality': ['exact'],
            'governorate': ['exact'],
            'marital_status': ['exact'],
            'sex': ['exact'],
        }
