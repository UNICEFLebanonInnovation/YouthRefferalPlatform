from django.utils.translation import ugettext as _

from django_filters import FilterSet, ModelChoiceFilter

from .models import Exporter


class ExporterFilter(FilterSet):

    class Meta:
        model = Exporter
        fields = {

        }
