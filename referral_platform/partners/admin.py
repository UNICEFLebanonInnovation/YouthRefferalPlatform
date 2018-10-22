from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import PartnerOrganization, Center


class PartnerOrganizationResource(resources.ModelResource):
    class Meta:
        model = PartnerOrganization
        fields = (
            'name',
            'phone_number',
            'email',
        )
        export_order = fields


class PartnerOrganizationAdmin(ImportExportModelAdmin):
    resource_class = PartnerOrganizationResource
    list_display = (
        'name',
        'locations_list',
        'phone_number',
        'email',
    )
    list_filter = (
        'locations',
    )
    search_fields = (
        'name',
    )
    filter_horizontal = ('locations',)

    def get_export_formats(self):
        from referral_platform.users.utils import get_default_export_formats
        return get_default_export_formats()


class CenterResource(resources.ModelResource):
    class Meta:
        model = Center
        fields = (
            'id',
            'name',
            'partner_organization',
        )
        export_order = fields


class CenterAdmin(ImportExportModelAdmin):
    resource_class = CenterResource
    list_display = (
        'id',
        'name',
        'partner_organization',
    )
    list_filter = (
        'partner_organization',
    )
    search_fields = (
        'name',
    )

    def get_export_formats(self):
        from referral_platform.users.utils import get_default_export_formats
        return get_default_export_formats()


admin.site.register(PartnerOrganization, PartnerOrganizationAdmin)
admin.site.register(Center, CenterAdmin)
