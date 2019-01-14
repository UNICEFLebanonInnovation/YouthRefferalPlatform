from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _

from django_filters import FilterSet, ModelChoiceFilter

from referral_platform.locations.models import Location
from referral_platform.youth.models import Nationality
from .models import YouthLedInitiative


class CommonFilter(FilterSet):

    governorate = ModelChoiceFilter(queryset=Location.objects.filter(parent__isnull=False),
                                    empty_label=_('Governorate'))

    # nationality = ModelChoiceFilter(queryset=Nationality.objects.all(), empty_label=_('Nationality'))


class YouthFilter(CommonFilter):

    class Meta:
        model = YouthLedInitiative
        fields = {
            'title': ['contains'],
            'location': ['contains'],
            'type': ['contains'],
            'Registration__first_name': ['contains'],
            'Registration__last_name': ['contains'],
        }
