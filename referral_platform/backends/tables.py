# coding: utf-8
import django_tables2 as tables
from django.utils.translation import ugettext as _

from .models import Exporter


class BootstrapTable(tables.Table):

    class Meta:
        model = Exporter
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class ExporterTable(tables.Table):

    class Meta:
        model = Exporter
        fields = (
            'name',
            'file_url',
            'created',
            'exported_by',
        )
