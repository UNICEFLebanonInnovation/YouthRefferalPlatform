# coding: utf-8
import django_tables2 as tables
from django.utils.translation import ugettext_lazy as _

from referral_platform.youth.models import YoungPerson


class BootstrapTable(tables.Table):

    class Meta:
        model = YoungPerson
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class CommonTable(tables.Table):

    edit_column = tables.TemplateColumn(verbose_name=_('Edit student'),
                                        template_name='django_tables2/edit_column.html',)

    class Meta:
        model = YoungPerson
        template = 'django_tables2/bootstrap.html'
        fields = (
            'edit_column',
            'first_name',
            'father_name',
            'last_name',
            'nationality',
            'address',
            'location',
        )

