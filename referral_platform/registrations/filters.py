from django.utils.translation import ugettext as _

from django_filters import FilterSet, ModelChoiceFilter

from referral_platform.locations.models import Location
from referral_platform.youth.models import Nationality
from .models import Registration


class CommonFilter(FilterSet):

    governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__isnull=False),
                                    empty_label=_('Governorate'))

    # nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))


class YouthFilter(CommonFilter):

    class Meta:
        model = Registration
        fields = {
            'youth__bayanati_ID': ['contains'],
            'location': ['contains'],
            'trainer': ['contains'],
            'youth__first_name': ['contains'],
            'youth__father_name': ['contains'],
            'youth__last_name': ['contains'],
            # 'nationality': ['exact'],
            'governorate': ['exact'],
            'youth__marital_status': ['exact'],
            'youth__sex': ['exact'],
        }


class YouthPLFilter(FilterSet):

    governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__p_code="PALESTINE"),
                                    empty_label=_('Governorate'))

    # nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))

    class Meta:
        model = Registration
        fields = {
            'location': ['contains'],
            'youth__first_name': ['contains'],
            'youth__father_name': ['contains'],
            'youth__last_name': ['contains'],
            # 'youth__nationality': ['exact'],
            'governorate': ['exact'],
            'youth__marital_status': ['exact'],
            'youth__sex': ['exact'],
        }


class YouthSYFilter(FilterSet):

    governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__p_code="SYRIA"),
                                    empty_label=_('Governorate'))

    # nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))

    class Meta:
        model = Registration
        fields = {
            'location': ['contains'],
            'youth__first_name': ['contains'],
            'youth__father_name': ['contains'],
            'youth__last_name': ['contains'],
            # 'youth__nationality': ['exact'],
            'governorate': ['exact'],
            'youth__marital_status': ['exact'],
            'youth__sex': ['exact'],
        }
