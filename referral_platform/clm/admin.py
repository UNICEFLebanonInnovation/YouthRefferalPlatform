from django.contrib import admin

from .models import (
    Assessment,
    AssessmentSubmission,
    Disability,
)

admin.site.register(Assessment)
admin.site.register(AssessmentSubmission)
# admin.site.register(Disability)

