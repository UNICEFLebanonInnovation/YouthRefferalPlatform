# coding: utf-8
import django_tables2 as tables
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _

from .models import Registration


class BootstrapTable(tables.Table):

    class Meta:
        model = Registration
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class CommonTable(tables.Table):

    edit_column = tables.TemplateColumn(verbose_name=_('Edit'), orderable=False,
                                        template_name='django_tables2/edit_column.html',
                                        attrs={'url': '/registrations/edit/'})
    # delete_column = tables.TemplateColumn(verbose_name=_('Delete'), orderable=False,
    #                                       template_name='django_tables2/delete_column.html',
    #                                       attrs={'url': '/api/registration/'})
    age = tables.Column(verbose_name=_('Age'), orderable=False, accessor='youth.calc_age')
    birthday = tables.Column(verbose_name=_('Birthday'), orderable=False, accessor='youth.birthday')

    class Meta:
        model = Registration
        fields = (
            'edit_column',
            # 'delete_column',
            'governorate',
            'trainer',
            'location',
            'youth.bayanati_ID',
            'youth.first_name',
            'youth.father_name',
            'youth.last_name',
            'youth.sex',
            'age',
            'birthday',
            'youth.nationality',
            'youth.marital_status',

            'center',
        )


class CommonTableAlt(tables.Table):

    edit_column = tables.TemplateColumn(verbose_name=_('Edit'), orderable=False,
                                        template_name='django_tables2/edit_column.html',
                                        attrs={'url': '/registrations/edit/'})
    # delete_column = tables.TemplateColumn(verbose_name=_('Delete'), orderable=False,
    #                                       template_name='django_tables2/delete_column.html',
    #                                       attrs={'url': '/api/registration/'})
    age = tables.Column(verbose_name=_('Age'), orderable=False, accessor='youth.calc_age')
    birthday = tables.Column(verbose_name=_('Birthday'), orderable=False, accessor='youth.birthday')

    class Meta:
        model = Registration
        fields = (
            'edit_column',
            # 'delete_column',
            'governorate',
            'location',
            'youth.first_name',
            'youth.father_name',
            'youth.last_name',
            'youth.sex',
            'age',
            'birthday',
            'youth.nationality',
            'youth.marital_status',

            'center',
        )
