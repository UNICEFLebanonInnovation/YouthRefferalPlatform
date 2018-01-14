from django.utils.translation import ugettext as _

from django_filters import FilterSet, ModelChoiceFilter

from referral_platform.locations.models import Location
from referral_platform.youth.models import Nationality
from .models import Registration


class CommonFilter(FilterSet):

    registration__governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__isnull=False),
                                    empty_label=_('Governorate'))

    # nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))


class YouthFilter(CommonFilter):

    class Meta:
        model = Registration
        fields = {
            'registration__youth__bayanati_ID': ['contains'],
            'registration__location': ['contains'],
            'registration__trainer': ['contains'],
            'registration__youth__first_name': ['contains'],
            'registration__youth__father_name': ['contains'],
            'registration__youth__last_name': ['contains'],
            # 'nationality': ['exact'],
            'registration__governorate': ['exact'],
            'registration__youth__marital_status': ['exact'],
            'registration__youth__sex': ['exact'],
        }


class YouthPLFilter(FilterSet):

    registration__governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__p_code="PALESTINE"),
                                    empty_label=_('Governorate'))

    # nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))

    class Meta:
        model = Registration
        fields = {
            'registration__location': ['contains'],
            'registration__youth__first_name': ['contains'],
            'registration__youth__father_name': ['contains'],
            'registration__youth__last_name': ['contains'],
            # 'youth__nationality': ['exact'],
            'registration__governorate': ['exact'],
            'youth__marital_status': ['exact'],
            'youth__sex': ['exact'],
        }


class YouthSYFilter(FilterSet):
    
    registration__governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__p_code="SYRIA"),
                                    empty_label=_('Governorate'))

    # nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))

    class Meta:
        model = Registration
        fields = {
            'registration__location': ['contains'],
            'registration__youth__first_name': ['contains'],
            'registration__youth__father_name': ['contains'],
            'registration__youth__last_name': ['contains'],
            # 'youth__nationality': ['exact'],
            'registration__governorate': ['exact'],
            'registration__youth__marital_status': ['exact'],
            'registration__youth__sex': ['exact'],
        }
