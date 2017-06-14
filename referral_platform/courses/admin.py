
from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from django.contrib.postgres.fields import JSONField

from prettyjson import PrettyJSONWidget

from .models import (
    Lab,
    Path,
    Course,
    Enrollment,
)


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class EnrollmentResource(resources.ModelResource):
    class Meta:
        model = Enrollment
        fields = (
            'youth',
            'course',
            'location',
            'enrolled',
            'pre_test_done',
            'post_test_done',
        )
        export_order = fields


class EnrollmentAdmin(ImportExportModelAdmin):
    resource_class = EnrollmentResource
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }
    list_display = (
        'youth',
        'course',
        'location',
        'enrolled',
        'pre_test_done',
        'post_test_done',
    )
    list_filter = (
        'status',
        'course',
        'location',
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


admin.site.register(Lab)
admin.site.register(Path, SlugAdmin)
admin.site.register(Course, SlugAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
