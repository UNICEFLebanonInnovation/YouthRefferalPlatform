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
                'partner_organization',
                'governorate',
                'trainer',
                'location',
                'first_name',
                'father_name',
                'last_name',
                'birthday_year',
                'birthday_month',
                'birthday_day',
                'sex',
                'nationality',
                'marital_status',
                'address',
            ]
        })
    ]

    suit_form_tabs = (
                      ('general', 'Basic Data'),
                    )

    list_display = (
        'partner_organization',
        'governorate',
        'trainer',
        'location',
        'first_name',
        'father_name',
        'last_name',
        'birthday_year',
        'birthday_month',
        'birthday_day',
        'sex',
        'nationality',
        'marital_status',
        'address',
        'created',
        'modified',
    )
    list_filter = (
        'partner_organization',
        'governorate',
        'sex',
        'nationality',
        'marital_status',
        'created',
        'modified',
    )
    search_fields = (
        'first_name',
        'last_name',
        'father_name'
    )


class NationalityResource(resources.ModelResource):

    class Meta:
        model = Nationality
        fields = (
            'id',
            'name',
            'code',
        )
        export_order = fields


class NationalityAdmin(ImportExportModelAdmin):
    resource_class = NationalityResource


admin.site.register(YoungPerson, YoungPersonAdmin)
# admin.site.register(EducationLevel)
admin.site.register(Nationality, NationalityAdmin)
# admin.site.register(IDType)
