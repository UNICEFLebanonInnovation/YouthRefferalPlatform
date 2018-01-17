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
    readonly_fields = (
        'youth',
        'youth_bayanati_ID',
        'youth_birthday',
        'youth_age',
        'youth_nationality',
        'youth_marital_status',
        'youth_address',
        'registration_assessment',
        'pre_civic_engagement',
        'post_civic_engagement',
        'initiative_registration',
        'initiative_implementation',
        'pre_entrepreneurship',
        'post_entrepreneurship',
    )
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'partner_organization',
                'governorate',
                'trainer',
                'center',
                'location',
                'youth',
                'youth_bayanati_ID',
                'youth_birthday',
                'youth_age',
                'youth_nationality',
                'youth_marital_status',
                'youth_address',
            ]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-assessment',),
            'fields': [
                'registration_assessment',
                'pre_civic_engagement',
                'post_civic_engagement',
                'initiative_registration',
                'initiative_implementation',
                'pre_entrepreneurship',
                'post_entrepreneurship',
                ]
        })
    ]

    suit_form_tabs = (
                      ('general', 'Basic Data'),
                      ('assessment', 'Assessments'),
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
            return qs.filter(partner_organization__locations=request.user.country.id)
        return qs

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        if has_group(request.user, 'UNICEF_CO'):
            return False
        return True

    def change_view(self, request, object_id, extra_context=None):
        self.save_as_continue = False
        if has_group(request.user, 'UNICEF_CO'):
            self.save_as_continue = False
            extra_context = extra_context or {}
            extra_context['readonly'] = True

        return super(RegistrationAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        if has_group(request.user, 'UNICEF_CO'):
            return self.readonly_fields + (
                'partner_organization',
                'governorate',
                'trainer',
                'center',
                'location',
            )
        return self.readonly_fields

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

    readonly_fields = (
        'youth',
        'registration'
    )

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
