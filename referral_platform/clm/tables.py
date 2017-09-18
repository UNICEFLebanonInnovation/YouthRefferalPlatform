# coding: utf-8
import django_tables2 as tables
from django.utils.translation import ugettext as _

from .models import CLM, BLN, RS, CBECE


class BootstrapTable(tables.Table):

    class Meta:
        model = CLM
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-bordered table-striped table-hover'}


class CommonTable(tables.Table):

    edit_column = tables.TemplateColumn(verbose_name=_('Edit student'),
                                        template_name='django_tables2/edit_column.html',
                                        attrs={'url': ''})
    delete_column = tables.TemplateColumn(verbose_name=_('Delete student'),
                                          template_name='django_tables2/delete_column.html',
                                          attrs={'url': ''})
    pre_assessment = tables.TemplateColumn(verbose_name=_('Pre-assessment'),
                                           template_name='django_tables2/clm_assessment.html',
                                           attrs={'url': ''})
    post_assessment = tables.TemplateColumn(verbose_name=_('Pre-assessment'),
                                            template_name='django_tables2/clm_assessment.html',
                                            attrs={'url': ''})

    student_age = tables.Column(verbose_name=_('Age'), accessor='student.age')
    student_birthday = tables.Column(verbose_name=_('Birthday'), accessor='student.birthday')

    class Meta:
        model = CLM
        template = 'django_tables2/bootstrap.html'
        fields = (
            'edit_column',
            'delete_column',
            'pre_assessment',
            'post_assessment',
            'student.first_name',
            'student.father_name',
            'student.last_name',
            'student.sex',
            'student_age',
            'student_birthday',
            'student.nationality',
            'student.mother_fullname',
            'student.address',
            'student.p_code',
        )


class BLNTable(CommonTable):

    edit_column = tables.TemplateColumn(verbose_name=_('Edit student'),
                                        template_name='django_tables2/edit_column.html',
                                        attrs={'url': '/clm/bln-edit/'})
    delete_column = tables.TemplateColumn(verbose_name=_('Delete student'),
                                          template_name='django_tables2/delete_column.html',
                                          attrs={'url': 'api/clm-bln/'})

    class Meta:
        model = BLN
        fields = CommonTable.Meta.fields


class RSTable(CommonTable):

    class Meta:
        model = RS


class CBECETable(CommonTable):

    class Meta:
        model = CBECE
