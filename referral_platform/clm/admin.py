from django.contrib import admin

from .models import (
    Assessment,
    Cycle,
    RSCycle,
    Site,
    Referral,
    Disability,
    BLN,
    RS,
    CBECE
)

admin.site.register(Assessment)
admin.site.register(Cycle)
admin.site.register(RSCycle)
admin.site.register(Site)
admin.site.register(Referral)
admin.site.register(Disability)
admin.site.register(BLN)
admin.site.register(RS)
admin.site.register(CBECE)
