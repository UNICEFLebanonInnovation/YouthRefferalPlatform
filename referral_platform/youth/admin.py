from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import *
import datetime

from . models import EducationLevel, IDType, Nationality, YoungPerson


class YoungPersonResource(resources.ModelResource):

    class Meta:
        model = YoungPerson
        fields = (

        )
        export_order = fields


class YoungPersonAdmin(ImportExportModelAdmin):
    resource_class = YoungPersonResource
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'first_name',
                'father_name',
                'last_name',
                'mother_firstname',
                'mother_lastname',
                'sex',
                'disability',
                # 'birthday_year',
                # 'birthday_month',
                # 'birthday_day',
                'phone',
                # 'phone_prefix',
                'parents_phone_number',
                'id_type',
                'id_number',
                'nationality',
                'mother_nationality',
                'location',
                'partner_organization',
                # 'address',
            ]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-educations',),
            'fields': [
                'education_status',
                'education_type',
                'education_level',
                'education_grade',
                'leaving_education_reasons',
            ]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-employments',),
            'fields': [
                'employment_status',
                'employment_sectors',
                'looking_for_work',
                'through_whom',
                'obstacles_for_work',
                'supporting_family',
                'household_composition',
                'household_working',
                'safety',
                'safety_reasons',
            ]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-followup',),
            'fields': [
                'trained_before',
                'not_trained_reason',
                'referred_by',
                'communication_preference',
            ]
        }),
    ]

    suit_form_tabs = (
                      ('general', 'Basic Data'),
                      ('educations', 'Educational Information'),
                      ('employments', 'Livelihood Information'),
                      ('followup', 'Follow-up Availability'),

                    )

    list_display = (
        '__unicode__',
        'mother_fullname',
        'birthday',
        'calc_age',
        'sex',
        'nationality',
        'location',
        'partner_organization',
        'education_status',
        'education_type',
        'education_level',
        'education_grade',
        'created',
        'modified',
    )
    list_filter = (
        'sex',
        'nationality',
        'location',
        'education_status',
        'education_type',
        'education_level',
        'education_grade',
        'created',
        'modified',
    )
    search_fields = (
        'first_name',
        'last_name',
        'father_name'
    )


admin.site.register(YoungPerson, YoungPersonAdmin)
admin.site.register(EducationLevel)
admin.site.register(Nationality)
admin.site.register(IDType)
