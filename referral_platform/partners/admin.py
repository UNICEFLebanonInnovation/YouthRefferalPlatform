from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import PartnerOrganization
from .models import Center


class PartnerOrganizationResource(resources.ModelResource):
    class Meta:
        model = PartnerOrganization
        fields = ()
        export_order = fields


class PartnerOrganizationAdmin(ImportExportModelAdmin):
    resource_class = PartnerOrganizationResource
    list_display = (
        'name',
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

    def get_queryset(self, request):
        qs = super(PartnerOrganizationAdmin, self).get_queryset(request)
        return qs


class CenterResource(ImportExportModelAdmin):
    class Meta:
        model = Center
        fields = ()
        export_order = fields


class CenterAdmin(ImportExportModelAdmin):
    resource_class = CenterResource
    list_display = (
        'name',
    )
    list_filter = (
        'partner_organization',
    )

    def get_queryset(self, request):
        qs = super(CenterAdmin, self).get_queryset(request)
        return qs


admin.site.register(PartnerOrganization, PartnerOrganizationAdmin)
admin.site.register(Center, CenterAdmin)
