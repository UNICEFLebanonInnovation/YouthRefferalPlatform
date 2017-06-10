
from django.contrib import admin

from .models import (
    Lab,
    Path,
    Course,
    Enrollment,
)

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'youth',
        'course',
        'location',
        'enrolled',
        'pre_test_done',
        'post_test_done',
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
