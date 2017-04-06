from django.contrib import admin

from . models import EducationLevel, IDType, Nationality, YoungPerson

admin.site.register(YoungPerson)
admin.site.register(EducationLevel)
admin.site.register(Nationality)
admin.site.register(IDType)
