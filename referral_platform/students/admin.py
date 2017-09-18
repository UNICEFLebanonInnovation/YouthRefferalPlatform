# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin
import datetime

from .models import (
    Student,
    StudentMatching,
    Nationality,
    IDType,
    Labour,
)
from .forms import StudentEnrollmentForm
from referral_platform.schools.models import (
    School,
    ClassRoom,
    EducationLevel,
    EducationYear,
    Section,
)
from referral_platform.locations.models import Location
from referral_platform.users.models import User


class NationalityResource(resources.ModelResource):
    class Meta:
        model = Nationality
        fields = (
            'id',
            'name',
        )
        export_order = ('name', )


class NationalityAdmin(ImportExportModelAdmin):
    resource_class = NationalityResource


class IDTypeResource(resources.ModelResource):
    class Meta:
        model = IDType
        fields = (
            'id',
            'name'
        )
        export_order = ('name', )


class IDTypeAdmin(ImportExportModelAdmin):
        resource_class = IDTypeResource

#
# class EnrollmentInline(admin.TabularInline):
#     model = Enrollment
#     extra = 0
#     fields = (
#         'education_year',
#         'school',
#         'section',
#         'classroom',
#         'registered_in_unhcr',
#         'last_education_level',
#         'last_school_type',
#         'last_school_shift',
#         'last_school',
#         'last_education_year',
#         'last_year_result',
#         'participated_in_alp',
#         'last_informal_edu_level',
#         'last_informal_edu_round',
#         'last_informal_edu_final_result',
#         'deleted',
#         'dropout_status',
#         # 'moved',
#     )


# class ALPInline(admin.TabularInline):
#     model = Outreach
#     extra = 0
#     fields = (
#         'alp_round',
#         'school',
#         'section',
#         'level',
#         'assigned_to_level',
#         'registered_in_level',
#         'refer_to_level',
#         'registered_in_unhcr',
#         'last_education_level',
#         'last_education_year',
#         'last_year_result',
#         'participated_in_alp',
#         'last_informal_edu_level',
#         'last_informal_edu_round',
#         'last_informal_edu_final_result',
#         'deleted',
#         'dropout_status',
#     )


class RegisteredInFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Registered in?'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'registered_in'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('pilot', 'PILOT'),
            ('alp', 'ALP'),
            ('2ndshift', '2nd-shift'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() and self.value() == 'pilot':
            return queryset.filter(referral_platform__isnull=False)
        if self.value() and self.value() == 'alp':
            return queryset.filter(
                alp_enrollment__isnull=False,
                alp_enrollment__deleted=False,
                alp_enrollment__dropout_status=False
            )
        if self.value() and self.value() == '2ndshift':
            return queryset.filter(
                student_enrollment__isnull=False,
                student_enrollment__deleted=False,
                student_enrollment__dropout_status=False
            )
        return queryset


class ALPhaseFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'ALP phase'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'alp_phase'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('outreach', 'Partner school outreach'),
            ('pretest', 'Pre-test'),
            ('current', 'Registered in school'),
            ('posttest', 'Post-test'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        alp_round = request.GET.get('alp_round', 0)
        if self.value():
            queryset = queryset.filter(
                alp_enrollment__isnull=False,
                alp_enrollment__alp_round=alp_round,
                alp_enrollment__deleted=False,
                alp_enrollment__dropout_status=False,

            )
        if self.value() and self.value() == 'outreach':
            users = User.objects.filter(groups__name__in=['PARTNER'])
            return queryset.filter(
                alp_enrollment__owner__in=users,
            )
        if self.value() and self.value() == 'pretest':
            not_schools = User.objects.filter(groups__name__in=['PARTNER', 'CERD'])
            return queryset.filter(
                alp_enrollment__owner__in=not_schools,
                alp_enrollment__level__isnull=False,
                alp_enrollment__assigned_to_level__isnull=False,
            )
        if self.value() and self.value() == 'current':
            return queryset.filter(
                alp_enrollment__registered_in_level__isnull=False,
            )
        if self.value() and self.value() == 'posttest':
            return queryset.filter(
                alp_enrollment__registered_in_level__isnull=False,
                alp_enrollment__refer_to_level__isnull=False,
            )
        return queryset


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
            if request.GET.get('registered_in', None) == 'alp':
                return queryset.filter(
                    alp_enrollment__school__location__parent_id=self.value(),
                    alp_enrollment__deleted=False,
                    alp_enrollment__dropout_status=False
                )
            elif request.GET.get('registered_in', None) == '2ndshift':
                return queryset.filter(
                    student_enrollment__school__location__parent_id=self.value(),
                    student_enrollment__deleted=False,
                    student_enrollment__dropout_status=False
                )
        return queryset


class DistrictFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'District'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'district'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l.id, l.name) for l in Location.objects.filter(type_id=2))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            if request.GET.get('registered_in', None) == 'alp':
                return queryset.filter(
                    alp_enrollment__school__location_id=self.value(),
                    alp_enrollment__deleted=False,
                    alp_enrollment__dropout_status=False
                )
            elif request.GET.get('registered_in', None) == '2ndshift':
                return queryset.filter(
                    student_enrollment__school__location_id=self.value(),
                    student_enrollment__deleted = False,
                    student_enrollment__dropout_status = False
                )
        return queryset


class SchoolFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'School'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'school'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l.id, l) for l in School.objects.filter())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            if request.GET.get('registered_in', None) == 'alp':
                return queryset.filter(
                    alp_enrollment__school_id=self.value(),
                    alp_enrollment__deleted=False,
                    alp_enrollment__dropout_status=False
                )
            elif request.GET.get('registered_in', None) == '2ndshift':
                return queryset.filter(
                    student_enrollment__school_id=self.value(),
                    student_enrollment__deleted=False,
                    student_enrollment__dropout_status=False
                )
        return queryset


class EducationYearFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Education Year'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'education_year'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l.id, l.name) for l in EducationYear.objects.filter())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(
                student_enrollment__education_year_id=self.value(),
                student_enrollment__deleted=False,
                student_enrollment__dropout_status=False
            )
        return queryset


class FormalEducationLevelFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Formal Education Level'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'education_level'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l.id, l.name) for l in ClassRoom.objects.filter())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(
                student_enrollment__classroom_id=self.value(),
                student_enrollment__deleted=False,
                student_enrollment__dropout_status=False
            )
        return queryset


class ALPLevelFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'ALP Level'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'alp_level'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l.id, l.name) for l in EducationLevel.objects.filter())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(alp_enrollment__registered_in_level_id=self.value())
        return queryset


class SectionFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Section'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l.id, l.name) for l in Section.objects.filter())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            if request.GET.get('registered_in', None) == 'alp':
                return queryset.filter(
                    alp_enrollment__section_id=self.value(),
                    alp_enrollment__deleted=False,
                    alp_enrollment__dropout_status=False
                )
            elif request.GET.get('registered_in', None) == '2ndshift':
                return queryset.filter(
                    student_enrollment__section_id=self.value(),
                    student_enrollment__deleted=False,
                    student_enrollment__dropout_status=False
                )
        return queryset


class ALPRoundFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'ALP Round'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'alp_round'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l.id, l.name) for l in ALPRound.objects.filter())

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            if request.GET.get('registered_in', None) == 'alp':
                return queryset.filter(
                    alp_enrollment__alp_round_id=self.value(),
                    alp_enrollment__registered_in_level__isnull=False,
                    alp_enrollment__deleted=False,
                    alp_enrollment__dropout_status=False
                )
        return queryset


class FromAgeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'From Age'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'from_age'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l, l) for l in range(0, 100))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            now = datetime.datetime.now()
            return queryset.filter(birthday_year__lte=(now.year - int(self.value())))

        return queryset


class ToAgeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'To Age'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'to_age'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return ((l, l) for l in range(0, 100))

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            now = datetime.datetime.now()
            return queryset.filter(birthday_year__gte=(now.year - int(self.value())))
        return queryset


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = (
            'first_name',
            'father_name',
            'last_name',
            'mother_fullname',
            'age',
            'birthday_day',
            'birthday_month',
            'birthday_year',
            'sex',
            'nationality',
            'mother_nationality',
            'id_type',
            'id_number',
            'number',
            'address',
            'phone',
            'phone_prefix',
        )
        export_order = (
            'first_name',
            'father_name',
            'last_name',
            'mother_fullname',
            'age',
            'birthday_day',
            'birthday_month',
            'birthday_year',
            'sex',
            'nationality',
            'mother_nationality',
            'id_type',
            'id_number',
            'number',
            'address',
            'phone',
            'phone_prefix',
        )


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    form = StudentEnrollmentForm
    list_display = (
        'first_name',
        'father_name',
        'last_name',
        'mother_fullname',
        'age',
        'sex',
        'nationality',
        'mother_nationality',
    )
    list_filter = (
        FromAgeFilter,
        ToAgeFilter,
        'birthday_day',
        'birthday_month',
        'birthday_year',
        'sex',
        'nationality',
        'mother_nationality',
        RegisteredInFilter,
        ALPRoundFilter,
        ALPhaseFilter,
        EducationYearFilter,
        SchoolFilter,
        FormalEducationLevelFilter,
        ALPLevelFilter,
        SectionFilter,
        DistrictFilter,
        GovernorateFilter,
    )
    search_fields = (
        'first_name',
        'father_name',
        'last_name',
        'mother_fullname',
        'id_number',
    )
    # inlines = (EnrollmentInline, ALPInline)


class StudentMatchingResource(resources.ModelResource):
    class Meta:
        model = StudentMatching


class StudentMatchingAdmin(ImportExportModelAdmin):
    resource_class = StudentMatching
    list_display = (
        'id',
        'pilot_id',
        'registry',
        'enrolled_id',
        'enrolment',
    )
    search_fields = (
        'registry__first_name',
        'registry__father_name',
        'registry__last_name',
        'registry__mother_fullname',
        'registry__id_number',
        'registry__number',
        'enrolment__first_name',
        'enrolment__father_name',
        'enrolment__last_name',
        'enrolment__mother_fullname',
        'enrolment__id_number',
        'enrolment__number',
    )

    def pilot_id(self, obj):
        if obj.registry:
            return obj.registry.id
        return ''

    def enrolled_id(self, obj):
        if obj.enrolment:
            return obj.enrolment.id
        return ''


admin.site.register(Student, StudentAdmin)
admin.site.register(Nationality, NationalityAdmin)
admin.site.register(StudentMatching, StudentMatchingAdmin)
admin.site.register(IDType, IDTypeAdmin)
admin.site.register(Labour)
