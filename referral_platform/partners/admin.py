
from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin

from .models import PartnerOrganization


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
    filter_horizontal = ('locations', )

    def get_queryset(self, request):
        qs = super(PartnerOrganizationAdmin, self).get_queryset(request)
        if request.user.partner:
            return qs.filter(id=request.user.partner.id)
        return qs


admin.site.register(PartnerOrganization, PartnerOrganizationAdmin)
