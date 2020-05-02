
from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from django.contrib.postgres.fields import JSONField
from referral_platform.registrations.models import Registration
from prettyjson import PrettyJSONWidget

from .models import YouthLedInitiative, AssessmentSubmission


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
#


class InitResource(resources.ModelResource):
    class Meta:
        model = YouthLedInitiative
        fields = (
            'title',
            # 'governorate',
            # 'partner_organization',
            # 'Participants',
            'id',


        )
        search_fields = (
            'title',
            'id',

        )
        export_order = fields


class InitAdmin(ImportExportModelAdmin):
    resource_class = InitResource
    list_display = (
        # 'partner_organization',
        'title',
        'partner_organization',
        'get_participants',
        'id',

    )
    list_filter = (
        'governorate',
        'partner_organization',
    )
    search_fields = (
        'title',
        'id',

    )

    # filter_horizontal = ('Participants',)


class AssessmentSubmissionResource(admin.ModelAdmin):
    class Meta:
        model = AssessmentSubmission
        fields = (
            'id',
            'initiative_id',
            'assessment',
            # 'member',
            'initiative',
            'data',
            'new_data',

        )
        export_order = fields

class AssessmentSubmissionAdmin(ImportExportModelAdmin):
    resource_class = AssessmentSubmissionResource
    list_display = (
        'id',
        'initiative_id',
        'assessment',
        # 'member',
        'initiative',

        'data',
        'new_data',
    )
    list_filter = (
        'assessment__name',
        'assessment__overview',
        'assessment__slug',

    )
    search_fields = (
        # 'member',
        'id',
        'initiative__title',
        'initiative__id',

    )

    def enrolled(self, obj):
        if obj.status == 'enrolled':
            return True
        return False
    enrolled.boolean = True

    def pre_test_done(self, obj):
        if obj.status == 'pre_test':
            return True
        return False
    pre_test_done.boolean = True

    def post_test_done(self, obj):
        if obj.status == 'post_test':
            return True
        return False
    post_test_done.boolean = True

admin.site.register(YouthLedInitiative, InitAdmin)
admin.site.register(AssessmentSubmission, AssessmentSubmissionAdmin)
#

