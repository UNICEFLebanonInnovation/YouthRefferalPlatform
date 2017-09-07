# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin

from .models import (
    School,
    EducationLevel,
    ClassLevel,
    Section,
    ClassRoom,
    PartnerOrganization,
    ALPReferMatrix,
    EducationYear,
    ALPAssignmentMatrix,
    EducationalLevel,
    Holiday
)
from referral_platform.locations.models import Location


class SchoolResource(resources.ModelResource):
    locationKazaa = fields.Field(column_name='District')
    locationGov = fields.Field(column_name='Governorate')

    class Meta:
        model = School
        fields = (
            'id',
            'name',
            'number',
            'location',
            'locationGov',
            'locationKazaa'
        )
        export_order = ('id', 'name', 'number', 'location', 'locationGov', 'locationKazaa')

    def dehydrate_locationKazaa(self, school):
        if school.location:
            return school.location.name
        return ''

    def dehydrate_locationGov(self, school):
        if school.location and school.location.parent:
            return school.location.parent.name
        return ''


class GovernorateFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Governorate'

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
        return ((l.id, l.name) for l in Location.objects.filter(type_id=1))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(location__parent_id=self.value())
        return queryset


class SchoolTypeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'School type'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'school_type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('alp', 'ALP'),
            ('2ndshift', '2nd shift'),
            ('both', 'ALP & 2nd shift'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if not self.value():
            return queryset
        if self.value() == 'alp':
            return queryset.filter(is_alp=True)
        if self.value() == '2ndshift':
            return queryset.filter(is_2nd_shift=True)
        if self.value() == 'both':
            return queryset.filter(is_alp=True, is_2nd_shift=True)


class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource
    list_display = (
        'name',
        'number',
        'location',
        'is_2nd_shift',
        'number_students_2nd_shift',
        'is_alp',
        'number_students_alp',
    )
    search_fields = (
        'name',
        'number',
    )
    list_filter = (
        SchoolTypeFilter,
        GovernorateFilter,
        'location',
    )

    actions = ('push_attendances_2ndshift', 'push_attendances_2ndshift_delay',
               'push_attendances_alp', 'push_attendances_alp_delay',)

    def push_attendances_2ndshift(self, request, queryset):
        for school in queryset:
            set_app_attendances(school_number=school.number)

    def push_attendances_2ndshift_delay(self, request, queryset):
        for school in queryset:
            set_app_attendances.delay(school_number=school.number)

    def push_attendances_alp(self, request, queryset):
        for school in queryset:
            set_app_attendances(school_number=school.number, school_type='alp')

    def push_attendances_alp_delay(self, request, queryset):
        for school in queryset:
            set_app_attendances.delay(school_number=school.number, school_type='alp')


class EducationLevelResource(resources.ModelResource):
    class Meta:
        model = EducationLevel
        fields = (
            'id',
            'name',
            'note',
        )
        export_order = ('name',)


class EducationLevelAdmin(ImportExportModelAdmin):
    resource_class = EducationLevelResource


class ClassLevelResource(resources.ModelResource):
    class Meta:
        model = ClassLevel
        fields = (
            'id',
            'name'
        )
        export_order = ('name',)


class ClassLevelAdmin(ImportExportModelAdmin):
    resource_class = ClassLevelResource


class SectionResource(resources.ModelResource):
    class Meta:
        model = Section
        fields = (
            'id',
            'name'
        )
        export_order = ('name',)


class SectionAdmin(ImportExportModelAdmin):
    resource_class = SectionResource


class ClassRoomResource(resources.ModelResource):
    class Meta:
        model = ClassRoom
        fields = (
            'id',
            'name',
        )
        export_order = fields


class ClassRoomAdmin(ImportExportModelAdmin):
    resource_class = ClassRoomResource
    fields = (
        'name',
    )
    list_display = fields


class PartnerOrganizationResource(resources.ModelResource):
    class Meta:
        model = PartnerOrganization
        fields = (
            'id',
            'name'
        )
        export_order = ('name',)


class PartnerOrganizationAdmin(ImportExportModelAdmin):
    resource_class = PartnerOrganizationResource
    search_fields = ('name', )


class ALPReferMatrixResource(resources.ModelResource):
    class Meta:
        model = ALPReferMatrix


class ALPReferMatrixAdmin(ImportExportModelAdmin):
    resource_class = ALPReferMatrixResource
    fields = (
        'level',
        'age',
        'success_refer_to',
        'fail_refer_to',
        'success_grade',
    )
    list_display = fields


class ALPAssignmentMatrixResource(resources.ModelResource):
    class Meta:
        model = ALPAssignmentMatrix


class ALPAssignmentMatrixAdmin(ImportExportModelAdmin):
    resource_class = ALPAssignmentMatrixResource
    fields = (
        'level',
        'range_start',
        'range_end',
        'refer_to',
    )
    list_display = (
        'level',
        'range',
        'refer_to',
    )


admin.site.register(School, SchoolAdmin)
admin.site.register(EducationLevel, EducationLevelAdmin)
admin.site.register(ClassLevel, ClassLevelAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(PartnerOrganization, PartnerOrganizationAdmin)
admin.site.register(ALPReferMatrix, ALPReferMatrixAdmin)
admin.site.register(EducationYear)
admin.site.register(Holiday)
admin.site.register(EducationalLevel)
admin.site.register(ALPAssignmentMatrix, ALPAssignmentMatrixAdmin)








