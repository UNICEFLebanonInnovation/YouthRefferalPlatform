
from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from django.contrib.postgres.fields import JSONField

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
            'member',
            'location',
            'partner_organization',
        )
        export_order = fields


class InitAdmin(ImportExportModelAdmin):
    resource_class = InitResource
    list_display = (
        'partner_organization',
        'title',
        'location',

    )
    list_filter = (
        'location',
    )
    search_fields = (
        'title',
    )
    filter_horizontal = ('member',)


    #
    # def enrolled(self, obj):
    #     if obj.status == 'enrolled':
    #         return True
    #     return False
    # enrolled.boolean = True
    #
    # def pre_test_done(self, obj):
    #     if obj.status == 'pre_test':
    #         return True
    #     return False
    # pre_test_done.boolean = True
    #
    # def post_test_done(self, obj):
    #     if obj.status == 'post_test':
    #         return True
    #     return False
    # post_test_done.boolean = True

class AssessmentSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        'assessment',
        'initiative',
        'data',
        'new_data',
    )
    list_filter = (
        'assessment__name',
        'assessment__overview',
        'assessment__slug',

    )


admin.site.register(YouthLedInitiative, InitAdmin)
admin.site.register(AssessmentSubmission, AssessmentSubmissionAdmin)
#

