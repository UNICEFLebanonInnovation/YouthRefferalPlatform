from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import *
import datetime

from .models import Registration, Assessment, AssessmentSubmission


class RegistrationResource(resources.ModelResource):

    class Meta:
        model = Registration
        fields = (

        )
        export_order = fields


class RegistrationAdmin(ImportExportModelAdmin):
    resource_class = RegistrationResource
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'partner_organization',
                'governorate',
                'trainer',
                'location',
                'youth__first_name',
                'youth__father_name',
                'youth__last_name',
                'youth__birthday_year',
                'youth__birthday_month',
                'youth__birthday_day',
                'youth__sex',
                'youth__nationality',
                'youth__marital_status',
                'youth__address',
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
        'youth',
        # 'youth__father_name',
        # 'youth__last_name',
        # 'youth__birthday_year',
        # 'youth__birthday_month',
        # 'youth__birthday_day',
        # 'youth__sex',
        # 'youth__nationality',
        # 'youth__marital_status',
        # 'youth__address',
        'created',
        'modified',
    )
    list_filter = (
        'partner_organization',
        'governorate',
        'youth__sex',
        'youth__nationality',
        'youth__marital_status',
        'created',
        'modified',
    )
    search_fields = (
        'youth__first_name',
        'youth__last_name',
        'youth__father_name'
    )


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Assessment)
admin.site.register(AssessmentSubmission)
