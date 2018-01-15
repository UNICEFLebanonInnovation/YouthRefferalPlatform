from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import *

from referral_platform.users.utils import has_group
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
                'youth',
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

    def get_queryset(self, request):
        qs = super(RegistrationAdmin, self).get_queryset(request)
        if has_group(request.user, 'UNICEF_CO'):
            return qs.filter(partner_organization__location=request.user.country)
        return qs

    def has_add_permission(self, request):
        if has_group(request.user, 'UNICEF_CO'):
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if has_group(request.user, 'UNICEF_CO'):
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if has_group(request.user, 'UNICEF_CO'):
            return False
        return True


class AssessmentAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
        'overview',
        'order',
    )
    list_filter = (
    )
    search_fields = (
    )


class AssessmentSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        'assessment',
        'registration',
        'data',
    )
    list_filter = (
        'assessment__name',
        'assessment__overview',
        'assessment__slug',
        'registration__partner_organization'
    )
    search_fields = (
        'youth__first_name',
        'youth__last_name',
        'youth__father_name',
        'youth__bayanati_ID'
    )


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(AssessmentSubmission, AssessmentSubmissionAdmin)
