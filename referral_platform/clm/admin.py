from django.contrib import admin

from .models import (
    Assessment,
    Disability,
)

admin.site.register(Assessment)
admin.site.register(Disability)

