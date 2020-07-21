# coding: utf-8
import django_tables2 as tables
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _

from .models import YouthLedent


class BootstrapTable(tables.Table):

    class Meta:
        model = YouthLedent
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class CommonTable(tables.Table):
    edit_column = tables.TemplateColumn(verbose_name=_('Edit'), orderable=False,
                                        template_name='django_tables2/edit_column.html',
                                        attrs={'url': '/initiatives/edit/'})
    # delete_column = tables.TemplateColumn(verbose_name=_('Delete'), orderable=False,
    #                                       template_name='django_tables2/delete_column.html',
    #                                       attrs={'url': '/api/initiatives/'})

    class Meta:
        model = YouthLedent
        fields = (
            'edit_column',
            'title',
            'Participants',
            'governorate',
            'type',
            'duration',

        )


class CommonTableAlt(tables.Table):
    class CommonTable(tables.Table):
        edit_column = tables.TemplateColumn(verbose_name=_('Edit'), orderable=False,
                                            template_name='django_tables2/edit_column.html',
                                            attrs={'url': '/initiatives/edit/'})

    class Meta:
        model = YouthLedent
        fields = (
            'edit_column',
            'title',
            'Participants',
            'governorate',
            'type',
            'duration',

        )
