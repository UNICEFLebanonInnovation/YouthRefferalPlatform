
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
from .exports import RegistrationFormat, RegistrationAssessmentFormat
from .models import Registration, Assessment, NewMapping, AssessmentSubmission, AssessmentHash


class BaseExportResource(resources.ModelResource):

    headers = []

    def insert_column(self, row, field_name, value):
        """
        Inserts a column into a row with a given value
        or sets a default value of empty string if none
        """
        row[field_name] = value if self.headers else ''

    # def insert_columns_inplace(self, row, fields, after_column):
    #     """
    #     Inserts fields with values into a row inplace
    #     and after a specific named column
    #     """
    #     keys = row.keys()
    #     before_column = None
    #     if after_column in row:
    #         index = keys.index(after_column)
    #         offset = index + 1
    #         if offset < len(row):
    #             before_column = keys[offset]
    #
    #     for key, value in fields.items():
    #         if before_column:
    #             row.insert(offset, key, value)
    #             offset += 1
    #         else:
    #             row[key] = value

    def fill_row(self, resource, fields):
        """
        This performs the actual work of translating
        a model into a fields dictionary for exporting.
        Inheriting classes must implement this.
        """
        return NotImplementedError()

    def export(self, queryset=None):
        """
        Exports a resource.
        """
        rows = []

        if queryset is None:
            queryset = self.get_queryset()

        fields = dict()

        for model in queryset.iterator():
            # first pass creates table shape
            self.fill_row(model, fields)

        self.headers = fields

        # Iterate without the queryset cache, to avoid wasting memory when
        # exporting large datasets.
        #TODO: review this and check performance
        for model in queryset.iterator():
            # second pass creates rows from the known table shape
            row = fields.copy()

            self.fill_row(model, row)

            rows.append(row)

        data = tablib.Dataset(headers=fields.keys())
        for row in rows:
            data.append(row.values())
        return data


class RegistrationResource(BaseExportResource):

    class Meta:
        model = Registration

    def fill_row(self, obj, row):
        self.insert_column(row, 'ID', obj.id)


class PartnerFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Partner Organisation')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'partner'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = PartnerOrganization.objects.all()
        if request.user.country:
            queryset = queryset.filter(locations=request.user.country_id)

        return ((l.id, l.name) for l in queryset)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(partner_organization_id=self.value())
        return queryset


class GovernorateFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Governorate')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'governorate'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = Location.objects.filter(parent__isnull=False)
        if request.user.country:
            queryset = queryset.filter(parent_id=request.user.country_id)

        return ((l.id, l.name) for l in queryset)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(governorate_id=self.value())
        return queryset


class RegistrationAdmin(ImportExportModelAdmin):
    resource_class = RegistrationResource
    formats = (
        RegistrationFormat,
        RegistrationAssessmentFormat,
    )
    readonly_fields = (
        'youth',
        'youth_bayanati_ID',
        'youth_birthday',
        'youth_age',
        'youth_nationality',
        'youth_marital_status',
        'youth_address',
        'registration_assessment',
        'pre_civic_engagement',
        'post_civic_engagement',
        'initiative_registration',
        'initiative_implementation',
        'pre_entrepreneurship',
        'post_entrepreneurship',
    )
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': [
                'partner_organization',
                'governorate',
                'trainer',
                'center',
                'location',
                'youth',
                'youth_bayanati_ID',
                'youth_birthday',
                'youth_age',
                'youth_nationality',
                'youth_marital_status',
                'youth_address',
            ]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-assessment',),
            'fields': [
                'registration_assessment',
                'pre_civic_engagement',
                'post_civic_engagement',
                'initiative_registration',
                'initiative_implementation',
                'pre_entrepreneurship',
                'post_entrepreneurship',
                ]
        })
    ]

    suit_form_tabs = (
                      ('general', 'Basic Data'),
                      ('assessment', 'Assessments'),
                    )

    list_display = (
        'partner_organization',
        'governorate',
        'trainer',
        'location',
        'youth',
        'created',
        'modified',
    )
    list_filter = (
        PartnerFilter,
        GovernorateFilter,
        'youth__sex',
        'youth__nationality',
        'youth__marital_status',
        'partner_organization',
        'created',
        'modified',
    )
    search_fields = (
        'youth__first_name',
        'youth__last_name',
        'youth__father_name'
    )

    def get_queryset(self, request):
        force_default_language(request)
        qs = super(RegistrationAdmin, self).get_queryset(request)
        if has_group(request.user, 'UNICEF_CO'):
            return qs.filter(partner_organization__locations=request.user.country.id)
        return qs

    def has_module_permission(self, request):
        return True

    def has_add_permission(self, request):
        if has_group(request.user, 'UNICEF_CO'):
            return False
        return True

    def change_view(self, request, object_id, extra_context=None):
        self.save_as_continue = False
        if has_group(request.user, 'UNICEF_CO'):
            self.save_as_continue = False
            extra_context = extra_context or {}
            extra_context['readonly'] = True

        return super(RegistrationAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        if has_group(request.user, 'UNICEF_CO'):
            return self.readonly_fields + (
                'partner_organization',
                'governorate',
                'trainer',
                'center',
                'location',
            )
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if has_group(request.user, 'UNICEF_CO'):
            return False
        return True


class AssessmentAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
        'overview',
        'order',
    )
    list_filter = (
    )
    search_fields = (
    )


# class NewMapping(resources.ModelResource):
#
#     class Meta:
#         model = NewMapping
#
#         fields = (
#             'type',
#             'key',
#             'old_value',
#             'new_value',
#         )
#         export_order = fields


class NewMappingAdmin(ImportExportModelAdmin):

    list_display = (
        'type',
        'key',
        'old_value',
        'new_value',
    )
    list_filter = (
        'type',
    )
    search_fields = (
        'type',
        'key',
    )


class AssessmentSubmissionAdmin(admin.ModelAdmin):

    readonly_fields = (
        'youth',
        'registration'
    )

    list_display = (
        'assessment',
        'registration',
        'data',
        'new_data',
    )
    list_filter = (
        'assessment__name',
        'assessment__overview',
        'assessment__slug',
        'registration__partner_organization'
    )
    search_fields = (
        'youth__first_name',
        'youth__last_name',
        'youth__father_name',
        'youth__bayanati_ID',
        'data',
        'new_data',
    )


class AssessmentHashAdmin(admin.ModelAdmin):

    readonly_fields = (

    )

    list_display = (
        'hashed',
        'registration',
        'assessment_slug',
        'partner',
    )
    list_filter = (
        'assessment_slug',
        'partner',
    )

    search_fields = (
        'hashed',
        'registration',
        'assessment_slug',

    )


admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(NewMapping, NewMappingAdmin)
admin.site.register(AssessmentSubmission, AssessmentSubmissionAdmin)
admin.site.register(AssessmentHash, AssessmentHashAdmin)
