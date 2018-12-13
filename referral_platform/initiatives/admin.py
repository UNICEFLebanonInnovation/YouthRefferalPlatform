import tablib


from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from import_export.widgets import *
from django.utils.translation import ugettext as _

from referral_platform.users.utils import has_group, force_default_language
from referral_platform.locations.models import Location
from referral_platform.partners.models import PartnerOrganization
from .models import YouthLedInitiative

# admin.site.register(YouthLedInitiative)
# class InitiativeResource(resources.ModelResource):
#     class Meta:
#         model = YouthLedInitiative
#         fields = (
#             'title',
#             'members',
#             'location',
#             'partner',
#             # 'pre_init_done',
#             # 'post_init_done',
#         )
#         export_order = fields
#


class InitResource(resources.ModelResource):
    class Meta:
        model = YouthLedInitiative
        fields = (
            'title',
            'members',
            'location',
        )
        export_order = fields


class InitAdmin(ImportExportModelAdmin):
    resource_class = InitResource
    list_display = (
        'title',
        'members',
        'location',

    )
    list_filter = (
        'location',
    )
    search_fields = (
        'title',
    )
    filter_horizontal = ('location',)


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


admin.site.register(YouthLedInitiative, InitAdmin)
#

