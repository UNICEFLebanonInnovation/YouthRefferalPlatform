# coding: utf-8
import django_tables2 as tables
from django.utils.translation import ugettext as _

from .models import YoungPerson


class BootstrapTable(tables.Table):

    class Meta:
        model = YoungPerson
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class CommonTable(tables.Table):

    edit_column = tables.TemplateColumn(verbose_name=_('Edit'), orderable=False,
                                        template_name='django_tables2/edit_column.html',
                                        attrs={'url': '/youth/edit/'})
    delete_column = tables.TemplateColumn(verbose_name=_('Delete'), orderable=False,
                                          template_name='django_tables2/delete_column.html',
                                          attrs={'url': '/youth/delete/'})
    age = tables.Column(verbose_name=_('age'), orderable=False, accessor='calc_age')
    birthday = tables.Column(verbose_name=_('Birthday'), orderable=False, accessor='birthday')

    class Meta:
        model = YoungPerson
        fields = (
            'edit_column',
            'delete_column',
            'governorate',
            'trainer',
            'location',
            'bayanati_ID',
            'first_name',
            'father_name',
            'last_name',
            'sex',
            'age',
            'birthday',
            'nationality',
            'marital_status',
            'address',
        )

#Creating Alternative table for Palestine and Syria
class CommonTableAlt(tables.Table):
            edit_column = tables.TemplateColumn(verbose_name=_('Edit'), orderable=False,
                                                template_name='django_tables2/edit_column.html',
                                                attrs={'url': '/youth/edit/'})
            delete_column = tables.TemplateColumn(verbose_name=_('Delete'), orderable=False,
                                                  template_name='django_tables2/delete_column.html',
                                                  attrs={'url': '/youth/delete/'})
            age = tables.Column(verbose_name=_('age'), orderable=False, accessor='calc_age')
            birthday = tables.Column(verbose_name=_('Birthday'), orderable=False, accessor='birthday')

            class Meta:
                model = YoungPerson
                fields = (
                    'edit_column',
                    'delete_column',
                    'governorate',
                    'location',
                    'first_name',
                    'father_name',
                    'last_name',
                    'sex',
                    'age',
                    'birthday',
                    'nationality',
                    'marital_status',
                    'address',
                )
