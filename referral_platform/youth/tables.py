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
                                        attrs={'url': '/clm/bln-edit/'})
    delete_column = tables.TemplateColumn(verbose_name=_('Delete'), orderable=False,
                                          template_name='django_tables2/delete_column.html',
                                          attrs={'url': '/api/clm-bln/'})
    age = tables.Column(verbose_name=_('age'), orderable=False, accessor='calc_age')
    birthday = tables.Column(verbose_name=_('Birthday'), orderable=False, accessor='birthday')

    # pre_assessment_result = tables.Column(verbose_name=_('Academic Result - Pre'), orderable=False,
    #                                       accessor='pre_test_score')
    # post_assessment_result = tables.Column(verbose_name=_('Academic Result - Post'), orderable=False,
    #                                        accessor='post_test_score')
    #
    # arabic_improvement = tables.Column(verbose_name=_('Arabic - Improvement'), orderable=False,
    #                                    accessor='arabic_improvement')
    # english_improvement = tables.Column(verbose_name=_('English - Improvement'), orderable=False,
    #                                     accessor='english_improvement')
    # french_improvement = tables.Column(verbose_name=_('French - Improvement'), orderable=False,
    #                                    accessor='french_improvement')
    # math_improvement = tables.Column(verbose_name=_('Math - Improvement'), orderable=False,
    #                                  accessor='math_improvement')
    #
    # assessment_improvement = tables.Column(verbose_name=_('Academic Result - Improvement'), orderable=False,
    #                                        accessor='assessment_improvement')

    class Meta:
        model = YoungPerson
        fields = (
            'edit_column',
            'delete_column',
            # 'round',
            # 'cycle',
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
            # 'pre_assessment_result',
            # 'post_assessment_result',
            # 'arabic_improvement',
            # 'english_improvement',
            # 'french_improvement',
            # 'math_improvement',
            # 'assessment_improvement',
            # 'participation',
            # 'learning_result',
            # 'owner',
            # 'modified_by',
            # 'created',
            # 'modified',
            # 'comments',
        )
