from django_filters import FilterSet

from referral_platform.youth.models import YoungPerson


class BLNFilter(FilterSet):
    class Meta:
        model = YoungPerson
        fields = {
            'first_name': ['contains'],
            'father_name': ['contains'],
            'last_name': ['contains'],
        }

