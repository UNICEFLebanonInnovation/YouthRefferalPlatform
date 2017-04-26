
from django.contrib import admin

from .models import (
    Lab,
    Course,
    Enrollment,
)

admin.site.register(Lab)
admin.site.register(Course)
admin.site.register(Enrollment)
