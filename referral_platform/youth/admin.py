from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import *
import datetime

from . models import Disability, IDType, Nationality, YoungPerson


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
                'partner_organization',
                'birthday_year',
                'birthday_month',
                'birthday_day',
                'sex',
                'nationality',
                'marital_status',
                'address',
                'number',
            ]
        })
    ]

    suit_form_tabs = (
                      ('general', 'Basic Data'),
                    )

    list_display = (
        'first_name',
        'father_name',
        'last_name',
        'partner_organization',
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

    def get_export_formats(self):
        from referral_platform.users.utils import get_default_export_formats
        return get_default_export_formats()


class NationalityResource(resources.ModelResource):

    class Meta:
        model = Nationality
        fields = (
            'id',
            'name',
            'name_en',
            'code',
        )

        export_order = fields


class NationalityAdmin(ImportExportModelAdmin):
    resource_class = NationalityResource
    list_display = (
        'id',
        'name',
        'name_en',
        'code',
    )

    def get_export_formats(self):
        from referral_platform.users.utils import get_default_export_formats
        return get_default_export_formats()

admin.site.register(YoungPerson, YoungPersonAdmin)
admin.site.register(Disability)
admin.site.register(Nationality, NationalityAdmin)
# admin.site.register(IDType)
