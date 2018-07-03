# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import tablib
import datetime
import time

from django.views.generic import ListView, FormView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import RedirectView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from referral_platform.backends.djqscsv import render_to_csv_response
from rest_framework import status
from rest_framework import viewsets, mixins, permissions
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin

from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin

from referral_platform.backends.tasks import *
from referral_platform.backends.exporter import export_full_data
from referral_platform.youth.models import YoungPerson
from .serializers import RegistrationSerializer, AssessmentSubmissionSerializer
from .models import Registration, Assessment, AssessmentSubmission, AssessmentHash
from .filters import YouthFilter, YouthPLFilter, YouthSYFilter
from .tables import BootstrapTable, CommonTable, CommonTableAlt
from .forms import CommonForm
from .mappings import *


class ListingView(LoginRequiredMixin,
                  FilterView,
                  ExportMixin,
                  SingleTableView,
                  RequestConfig):

    table_class = CommonTable
    model = Registration
    template_name = 'registrations/list.html'
    table = BootstrapTable(Registration.objects.all(), order_by='id')

    filterset_class = YouthFilter

    def get_queryset(self):
        return Registration.objects.filter(partner_organization=self.request.user.partner)

    def get_filterset_class(self):
        locations = [g.p_code for g in self.request.user.partner.locations.all()]
        if "PALESTINE" in locations:
            return YouthPLFilter
        elif "SYRIA" in locations:
            return YouthSYFilter
        elif "JORDAN" in locations:
            return YouthFilter

    def get_table_class(self):
            locations = [g.p_code for g in self.request.user.partner.locations.all()]
            if "PALESTINE" in locations:
                return CommonTableAlt
            elif "SYRIA" in locations:
                return CommonTableAlt
            elif "JORDAN" in locations:
                return CommonTable


class AddView(LoginRequiredMixin, FormView):

    template_name = 'registrations/form.html'
    form_class = CommonForm
    model = Registration
    success_url = '/registrations/list/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/registrations/add/'
        return self.success_url

    def get_initial(self):
        # force_default_language(self.request, 'ar-ar')
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner

        if self.request.GET.get('youth_id'):
                instance = YoungPerson.objects.get(id=self.request.GET.get('youth_id'))
                data['youth_id'] = instance.id
                data['youth_first_name'] = instance.first_name
                data['youth_father_name'] = instance.father_name
                data['youth_last_name'] = instance.last_name
                data['youth_birthday_day'] = instance.birthday_day
                data['youth_birthday_month'] = instance.birthday_month
                data['youth_birthday_year'] = instance.birthday_year
                data['youth_sex'] = instance.sex
                data['youth_nationality'] = instance.nationality_id
                data['youth_marital_status'] = instance.marital_status

        initial = data
        return initial

    def form_valid(self, form):
        form.save(request=self.request)
        return super(AddView, self).form_valid(form)


class EditView(LoginRequiredMixin, FormView):
    template_name = 'registrations/form.html'
    form_class = CommonForm
    model = Registration
    success_url = '/registrations/list/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/registrations/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def get_form(self, form_class=None):
        instance = Registration.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
        if self.request.method == "POST":
            return CommonForm(self.request.POST, instance=instance)
        else:
            data = RegistrationSerializer(instance).data
            data['youth_nationality'] = data['youth_nationality_id']
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
            return CommonForm(data, instance=instance)

    def form_valid(self, form):
        instance = Registration.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
        form.save(request=self.request, instance=instance)
        return super(EditView, self).form_valid(form)


class YouthAssessment(SingleObjectMixin, RedirectView):
    model = Assessment

    def get_redirect_url(self, *args, **kwargs):
        assessment = self.get_object()
        registry = Registration.objects.get(id=self.request.GET.get('registry'),
                                            partner_organization=self.request.user.partner)
        youth = registry.youth
        hashing = AssessmentHash.objects.create(
            registration=registry.id,
            assessment_slug=assessment.slug,
            partner=self.request.user.partner_id,
            user=self.request.user.id,
            timestamp=time.time()
        )

        url = '{form}?d[registry]={registry}&d[country]={country}&d[partner]={partner}&d[nationality]={nationality}' \
              '&returnURL={callback}'.format(
                form=assessment.assessment_form,
                registry=hashing.hashed,
                partner=registry.partner_organization.name,
                country=registry.governorate.parent.name,
                nationality=youth.nationality.code,
                callback=self.request.META.get('HTTP_REFERER', registry.get_absolute_url())
        )
        return url


@method_decorator(csrf_exempt, name='dispatch')
class YouthAssessmentSubmission(SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        if 'registry' not in request.body:
            return HttpResponseBadRequest()

        payload = json.loads(request.body.decode('utf-8'))

        hashing = AssessmentHash.objects.get(hashed=payload['registry'])

        registration = Registration.objects.get(id=int(hashing.registration))
        assessment = Assessment.objects.get(slug=hashing.assessment_slug)
        submission, new = AssessmentSubmission.objects.get_or_create(
            registration=registration,
            youth=registration.youth,
            assessment=assessment,
            status='enrolled'
        )
        submission.data = payload
        submission.save()

        return HttpResponse()


class RegistrationViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):

    model = Registration
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.method in ["PATCH", "POST", "PUT"]:
            return self.queryset
        return self.queryset.filter(partner_organization=self.request.user.partner)

    def delete(self, request, *args, **kwargs):
        instance = self.model.objects.get(id=kwargs['pk'], partner_organization=self.request.user.partner)
        instance.delete()
        return JsonResponse({'status': status.HTTP_200_OK})


class AssessmentSubmissionViewSet(mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.all()
    serializer_class = AssessmentSubmissionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExportView(LoginRequiredMixin, ListView):

    model = Registration
    queryset = Registration.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser and not self.request.user.partner:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            queryset = queryset.filter(governorate_id=int(gov))
        country = self.request.GET.get('country', 0)
        if country:
            queryset = queryset.filter(partner_organization__locations=int(country))

    def get(self, request, *args, **kwargs):

        # if self.request.user.is_superuser and not self.request.user.partner:
        #     queryset = self.queryset
        # else:
        #     queryset = self.queryset.filter(partner_organization=self.request.user.partner)
        #
        # gov = self.request.GET.get('governorate', 0)
        # if gov:
        #     queryset = queryset.filter(governorate_id=int(gov))
        # country = self.request.GET.get('country', 0)
        # if country:
        #     queryset = queryset.filter(partner_organization__locations=int(country))

        headers = {
            # 'self__country': 'Country',
            'youth__governorate': 'Governorate',
            'youth__Location': 'Location',
            'youth__partner_organization': 'Partner',
            # 'youth__number': 'Unique number',
            'youth__first_name': 'First Name',
            'youth__ father_name': "Father's Name",
            'youth__ last_name': 'Last Name',
            'youth__trainer': 'Trainer',
            'youth__bayanati_ID': 'Bayanati ID',
            # 'youth__number': 'Jordanian ID',
            'youth__sex': 'Gender',
            'youth__birthday_day': 'birthday day',
            'youth__birthday_month': 'birthday month',
            'youth__birthday_year': 'birthday year',
            'youth__age': 'age',
            'youth__elapsed_years': 'Date of birth',
            'youth__nationality': 'Nationality',
            'youth__marital_status': 'Marital status',
            'youth__address': 'address',
            # 'registration__number': 'Submission date',
            'youth__center':  'Center',
    }
        qs = self.get_queryset().values(
            # 'self__country',
            'youth__governorate',
            'youth__Location',
            'youth__partner_organization',
            # 'youth__number': 'Unique number',
            'youth__first_name',
            'youth__ father_name',
            'youth__ last_name',
            'youth__trainer',
            'youth__bayanati_ID',
            # 'youth__number': 'Jordanian ID',
            'youth__sex',
            'youth__birthday_day',
            'youth__birthday_month',
            'youth__birthday_year',
            'youth__age',
            'youth__elapsed_years',
            'youth__nationality',
            'youth__marital_status',
            'youth__address',
            # 'registration__number': 'Submission date',
            'youth__center',
        )

        return render_to_csv_response(qs, field_header_map=headers)

        #
        # book = tablib.Databook()
        # data = tablib.Dataset()
        # data.title = "Beneficiary List"
        # data.headers = common_headers
        #
        # content = []
        # for line in queryset:
        #     youth = line.youth
        #     content = [
        #         line.governorate.parent.name if line.governorate else '',
        #         line.governorate.name if line.governorate else '',
        #         line.location,
        #         line.partner_organization.name if line.partner_organization else '',
        #
        #         youth.number,
        #         youth.first_name,
        #         youth.father_name,
        #         youth.last_name,
        #         line.trainer,
        #         youth.bayanati_ID,
        #         youth.id_number,
        #         youth.sex,
        #         youth.birthday_day,
        #         youth.birthday_month,
        #         youth.birthday_year,
        #         youth.calc_age,
        #         youth.birthday,
        #         youth.nationality.name,
        #         youth.marital_status,
        #         youth.address,
        #         line.created.strftime('%d/%m/%Y') if line.created else '',
        #     ]
        #     data.append(content)
        #
        # book.add_sheet(data)
        #
        # response = HttpResponse(
        #     book.export("xls"),
        #     content_type='application/vnd.ms-excel',
        # )
        # response['Content-Disposition'] = 'attachment; filename=Beneficiary_list.xls'
        # return response


class ExportRegistryAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.filter(assessment__slug='registration')

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()

        if self.request.user.is_superuser and not self.request.user.partner:
            submission_set = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            submission_set = submission_set.filter(registration__governorate_id=int(gov))
        country = self.request.GET.get('country', 0)
        if country:
            submission_set = submission_set.filter(registration__partner_organization__locations=int(country))

        data2 = tablib.Dataset()
        data2.title = "Registration Assessment"
        data2.headers = [
            'Country',
            'Governorate',
            'Location',
            'Partner',

            'Unique number',
            'First Name',
            "Father's Name",
            'Last Name',
            'Trainer',
            'Bayanati ID',
            'Jordanian ID',
            'Gender',
            'birthday day',
            'birthday month',
            'birthday year',
            'age',
            'Date of birth',
            'Nationality',
            'Marital status',
            'address',

            'Type of training',
            'Type of center',
            'center ID',
            'Conscent form filled',
            'If you answered Others, provide the name of the NGO',

            'UNHCR ID',
            'Jordanian ID',
            'Starting date of training',
            'Ending date of Training',
            'Education status',

            'Current education level',
            'Type of school',
            'School name',

            'If you are attending school, how many times have you missed your classes in the past 3 months',
            'Reasons for skipping school more than once',
            'Education level completed before leaving school',

            'Reasons for leaving school',
            # 'fam_request',
            # 'underachieveme',
            # 'illness',
            # 'school_far',
            # 'expenses',
            # 'unsafe_travel',
            # 'engaged_for_mo',
            # 'educ_no_help',
            # 'not_space',
            # 'low_standard',
            # 'school_bullyin',
            # 'other',

            'If you answered (Others), what is the reason?',

            'Relationship with Labour Market',
            'Type of occupation',

            'Owned electronic devices',
            'laptop',
            'computer',
            'smart_phone',
            'tablet',
            'NA',

            'Family composition',
            'mother',
            'father',
            'brothers',
            'sisters',
            'other_relative',
            'na',
            'orphan',

            'the above household members are not living with you at the moment',

            'If your answer is yes please specify why',
            'If other, please specify',
            'Any family member use drug/alcohol?',
            'Feeling of safety',

            'Reasons for not feeling safe most or all of the time',
            # 'conflict_relat',
            # 'violence_home',
            # 'comm_viol_harr',
            # 'unplanned_futu',
            # 'school_viol_ha',
            # 'other',

            'Accommodation type',
            'Displacement status',

            'Family members who have a fixed income source',
            'mother',
            'father',
            'brothers',
            'sisters',
            'none_of_them',
            'NA',

            'Preferred method of communication for follow up',
            'facebook',
            'email',
            'mobile_phone',
            'through_NGO',
            'no_follow_up',

            'Facebook account',
            'Email address',
            'Mobile phone number',
            'submission_time',
        ]

        for line2 in submission_set:
            content = []
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.id_number,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                get_choice_value(line2.data, 'training_type'),
                get_choice_value(line2.data, 'center_type'),
                registry.center.name if registry.center else '',
                get_choice_value(line2.data, 'concent_paper', 'status'),
                line2.data.get('If_you_answered_Othe_the_name_of_the_NGO', ''),

                line2.data.get('UNHCR_ID', ''),
                line2.data.get('Jordanian_ID', ''),
                line2.data.get('training_date', ''),
                line2.data.get('training_end_date', ''),
                get_choice_value(line2.data, 'educational_status'),

                get_choice_value(line2.data, 'school_level'),
                get_choice_value(line2.data, 'School_type'),
                line2.data.get('School_name', ''),

                get_choice_value(line2.data, 'how_many_times_skipped_school', 'how_many'),
                line2.data.get('reason_for_skipping_class', ''),
                get_choice_value(line2.data, 'educ_level_stopped'),

                get_choice_value(line2.data, 'Reason_stop_study'),
                # line2.data.get('Reason_stop_study', ''),
                # line2.get_data_option('Reason_stop_study', 'fam_request'),
                # line2.get_data_option('Reason_stop_study', 'underachieveme'),
                # line2.get_data_option('Reason_stop_study', 'illness'),
                # line2.get_data_option('Reason_stop_study', 'school_far'),
                # line2.get_data_option('Reason_stop_study', 'expenses'),
                # line2.get_data_option('Reason_stop_study', 'unsafe_travel'),
                # line2.get_data_option('Reason_stop_study', 'engaged_for_mo'),
                # line2.get_data_option('Reason_stop_study', 'educ_no_help'),
                # line2.get_data_option('Reason_stop_study', 'not_space'),
                # line2.get_data_option('Reason_stop_study', 'low_standard'),
                # line2.get_data_option('Reason_stop_study', 'school_bullyin'),
                # line2.get_data_option('Reason_stop_study', 'other'),

                line2.data.get('other_five', ''),

                get_choice_value(line2.data, 'Relation_with_labor_market'),
                get_choice_value(line2.data, 'occupation_type'),

                # get_choice_value(line2.data, 'what_electronics_do_you_own'),
                line2.data.get('what_electronics_do_you_own', ''),
                line2.get_data_option('what_electronics_do_you_own', 'laptop'),
                line2.get_data_option('what_electronics_do_you_own', 'computer'),
                line2.get_data_option('what_electronics_do_you_own', 'smart_phone'),
                line2.get_data_option('what_electronics_do_you_own', 'tablet'),
                line2.get_data_option('what_electronics_do_you_own', 'NA'),

                # get_choice_value(line2.data, 'family_present', 'family'),
                line2.data.get('family_present', ''),
                line2.get_data_option('family_present', 'mother'),
                line2.get_data_option('family_present', 'father'),
                line2.get_data_option('family_present', 'brothers'),
                line2.get_data_option('family_present', 'sisters'),
                line2.get_data_option('family_present', 'other_relative'),
                line2.get_data_option('family_present', 'na'),
                line2.get_data_option('family_present', 'orphan'),

                get_choice_value(line2.data, 'family_not_present', 'yes_no'),

                get_choice_value(line2.data, 'not_present_where'),
                line2.data.get('other_family_not_present', ''),
                get_choice_value(line2.data, 'drugs_substance_use', 'yes_no'),
                get_choice_value(line2.data, 'feeling_of_safety_security', 'feeling_safety'),

                get_choice_value(line2.data, 'reasons_for_not_feeling_safe_a', 'not_feeling_safety'),
                # line2.data.get('reasons_for_not_feeling_safe_a', ''),
                # line2.get_data_option('reasons_for_not_feeling_safe_a', 'conflict_relat'),
                # line2.get_data_option('reasons_for_not_feeling_safe_a', 'violence_home'),
                # line2.get_data_option('reasons_for_not_feeling_safe_a', 'comm_viol_harr'),
                # line2.get_data_option('reasons_for_not_feeling_safe_a', 'unplanned_futu'),
                # line2.get_data_option('reasons_for_not_feeling_safe_a', 'school_viol_ha'),
                # line2.get_data_option('reasons_for_not_feeling_safe_a', 'other'),

                get_choice_value(line2.data, 'Accommodation_type'),
                get_choice_value(line2.data, 'how_many_times_displaced', 'how_many'),
                # get_choice_value(line2.data, 'family_steady_income', 'family'),
                line2.data.get('family_steady_income', ''),
                line2.get_data_option('family_steady_income', 'mother'),
                line2.get_data_option('family_steady_income', 'father'),
                line2.get_data_option('family_steady_income', 'brothers'),
                line2.get_data_option('family_steady_income', 'sisters'),
                line2.get_data_option('family_steady_income', 'none_of_them'),
                line2.get_data_option('family_steady_income', 'NA'),

                # get_choice_value(line2.data, 'desired_method_for_follow_up', 'method_follow_up'),
                line2.data.get('desired_method_for_follow_up', ''),
                line2.get_data_option('desired_method_for_follow_up', 'facebook'),
                line2.get_data_option('desired_method_for_follow_up', 'email'),
                line2.get_data_option('desired_method_for_follow_up', 'mobile_phone'),
                line2.get_data_option('desired_method_for_follow_up', 'through_NGO'),
                line2.get_data_option('desired_method_for_follow_up', 'no_follow_up'),

                line2.data.get('text_39911992', ''),
                line2.data.get('text_d45750c6', ''),
                line2.data.get('text_4c6fe6c9', ''),
                submission_date,
            ]
            data2.append(content)

        book.add_sheet(data2)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_Registration_Assessments.xls'
        return response


class ExportCivicAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.all()

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()

        if self.request.user.is_superuser and not self.request.user.partner:
            submission_set = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            submission_set = submission_set.filter(registration__governorate_id=int(gov))
        country = self.request.GET.get('country', 0)
        if country:
            submission_set = submission_set.filter(registration__partner_organization__locations=int(country))

        data3 = tablib.Dataset()
        data3.title = "Pre-Assessment"
        data3.headers = [
            'Country',
            'Governorate',
            'Location',
            'Partner',

            'Unique number',
            'First Name',
            "Father's Name",
            'Last Name',
            'Trainer',
            'Bayanati ID',
            'Jordanian ID',
            'Gender',
            'birthday day',
            'birthday month',
            'birthday year',
            'age',
            'Date of birth',
            'Nationality',
            'Marital status',
            'address',

            'I can articulate/state my thoughts, feelings and ideas to others well',
            'I can express my opinions when my classmates/friends/peers disagree with me',
            'Usually I discuss with friends/parents/colleagues to clarify some issues before taking a decision in that regard',
            'I build on the ideas of others.',
            'I am willing to compromise my own view to obtain a group consensus.',
            'I feel I belong to my community',
            'I know where to volunteer in my community',
            'I volunteer on a regular basis in my community',
            'I feel I am appreciated for my contributions to my community.',
            'I believe I can contribute towards the development (betterment) of my community',
            'I am able to address/discuss community concerns in interactions with community leaders/people of authority at the local level',
            'I participate actively in addressing my community concerns through media/social media',
            'submission time',
        ]

        data4 = tablib.Dataset()
        data4.title = "Post-Assessment"
        data4.headers = [
            'Country',
            'Governorate',
            'Location',
            'Partner',

            'Unique number',
            'First Name',
            "Father's Name",
            'Last Name',
            'Trainer',
            'Bayanati ID',
            'Jordanian ID',
            'Gender',
            'birthday day',
            'birthday month',
            'birthday year',
            'age',
            'Date of birth',
            'Nationality',
            'Marital status',
            'address',

            'I can articulate/state my thoughts, feelings and ideas to others well',
            'I can express my opinions when my classmates/friends/peers disagree with me',
            'Usually I discuss with friends/parents/colleagues to clarify some issues before taking a decision in that regard',
            'I build on the ideas of others.',
            'I am willing to compromise my own view to obtain a group consensus.',
            'I feel I belong to my community',
            'I know where to volunteer in my community',
            'I volunteer on a regular basis in my community',
            'I feel I am appreciated for my contributions to my community.',
            'I believe I can contribute towards the development (betterment) of my community',
            'I am able to address/discuss community concerns in interactions with community leaders/people of authority at the local level',
            'I participate actively in addressing my community concerns through media/social media',
            'submission time'
        ]

        submission_set1 = submission_set.filter(assessment__slug='pre_assessment')
        for line2 in submission_set1:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.id_number,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                get_choice_value(line2.data, '_4_articulate_thoughts', 'rates'),
                get_choice_value(line2.data, '_1_express_opinion', 'rates'),
                get_choice_value(line2.data, 'discuss_before_decision', 'rates'),
                get_choice_value(line2.data, '_28_discuss_opinions', 'rates'),
                get_choice_value(line2.data, '_31_willing_to_compromise', 'rates'),
                get_choice_value(line2.data, '_pal_I_belong', 'rates'),
                get_choice_value(line2.data, '_41_where_to_volunteer', 'rates'),
                get_choice_value(line2.data, '_42_regularly_volunteer', 'rates'),
                get_choice_value(line2.data, '_pal_contrib_appreciated', 'rates'),
                get_choice_value(line2.data, '_pal_contribute_to_development', 'rates'),
                get_choice_value(line2.data, '_51_communicate_community_conc', 'rates'),
                get_choice_value(line2.data, '_52_participate_community_medi', 'rates'),
                submission_date,
            ]
            data3.append(content)

        submission_set2 = submission_set.filter(assessment__slug='post_assessment')
        for line2 in submission_set2:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.id_number,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                get_choice_value(line2.data, '_4_articulate_thoughts', 'rates'),
                get_choice_value(line2.data, '_1_express_opinion', 'rates'),
                get_choice_value(line2.data, 'discuss_before_decision', 'rates'),
                get_choice_value(line2.data, '_28_discuss_opinions', 'rates'),
                get_choice_value(line2.data, '_31_willing_to_compromise', 'rates'),
                get_choice_value(line2.data, '_pal_I_belong', 'rates'),
                get_choice_value(line2.data, '_41_where_to_volunteer', 'rates'),
                get_choice_value(line2.data, '_42_regularly_volunteer', 'rates'),
                get_choice_value(line2.data, '_pal_contrib_appreciated', 'rates'),
                get_choice_value(line2.data, '_pal_contribute_to_development', 'rates'),
                get_choice_value(line2.data, '_51_communicate_community_conc', 'rates'),
                get_choice_value(line2.data, '_52_participate_community_medi', 'rates'),
                submission_date,
            ]
            data4.append(content)

        book.add_sheet(data3)
        book.add_sheet(data4)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_Civic_Engagement_Assessments.xls'
        return response


class ExportEntrepreneurshipAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.all()

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()

        if self.request.user.is_superuser and not self.request.user.partner:
            submission_set = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            submission_set = submission_set.filter(registration__governorate_id=int(gov))
        country = self.request.GET.get('country', 0)
        if country:
            submission_set = submission_set.filter(registration__partner_organization__locations=int(country))

        data5 = tablib.Dataset()
        data5.title = "Pre-Entrepreneurship"
        data5.headers = [
            'Country',
            'Governorate',
            'Location',
            'Partner',

            'Unique number',
            'First Name',
            "Father's Name",
            'Last Name',
            'Trainer',
            'Bayanati ID',
            'Jordanian ID',
            'Gender',
            'birthday day',
            'birthday month',
            'birthday year',
            'age',
            'Date of birth',
            'Nationality',
            'Marital status',
            'address',

            'I am prepared to plan my personal objectives',
            'I am prepared to plan my professional objectives',
            'I know how to manage my monetary affairs responsibly',
            'I know ways to plan my time',
            'I can give suggestions without being bossy',
            'I make a decision by thinking about all the information I have about available options decision making',
            'I know how to identify causes for my problems and find solutions for them  problem solving',
            'I know where and when to get support when I face a problem',
            'When I am stressed, I manage my stress in a positive way',
            'There are opportunities in the labour market that encourage me to develop my skills',

            'A good communicator',
            'The most important part of delivering a successful presentation is',

            'A team is a group of people who',
            'To work efficiently as a team',
            'If I am the group leader, I will',
            'One of the main reasons to NOT make the best decision',
            'The easiest solution for the problem is always the best solution',
            'If you face a problem, what procedures would you take into consideration to solve the problem? Please arrange the below steps chronologically',
            'submission time',
        ]

        data6 = tablib.Dataset()
        data6.title = "Post-Entrepreneurship"
        data6.headers = [
            'Country',
            'Governorate',
            'Location',
            'Partner',

            'Unique number',
            'First Name',
            "Father's Name",
            'Last Name',
            'Trainer',
            'Bayanati ID',
            'Jordanian ID',
            'Gender',
            'birthday day',
            'birthday month',
            'birthday year',
            'age',
            'Date of birth',
            'Nationality',
            'Marital status',
            'address',

            'I am prepared to plan my personal objectives',
            'I am prepared to plan my professional objectives',
            'I know how to manage my monetary affairs responsibly',
            'I know ways to plan my time',
            'I can give suggestions without being bossy',
            'I make a decision by thinking about all the information I have about available options decision making',
            'I know how to identify causes for my problems and find solutions for them  problem solving',
            'I know where and when to get support when I face a problem',
            'When I am stressed, I manage my stress in a positive way',
            'There are opportunities in the labour market that encourage me to develop my skills',

            'A good communicator',
            'The most important part of delivering a successful presentation is',

            'A team is a group of people who',
            'To work efficiently as a team',
            'If I am the group leader, I will',
            'One of the main reasons to NOT make the best decision',
            'The easiest solution for the problem is always the best solution',
            'If you face a problem, what procedures would you take into consideration to solve the problem?',
            'Rate the benefits of the training to your personal life',
            'Have you faced any challenges with the program?',

            'Challenges',
            'The program materials/design were difficult to understand',
            'The facilitators didn\'t provide us with required support',
            'The training period is too short',
            'The training period is too long',
            'Meeting room/location not convenient',

            'If the room/ training area not convenient, please specify why',
            'Location of CBO is too far',
            'The rooms are not very well ventilated',
            'The rooms are not clean',
            'There are no tables / chairs',
            'The classroom lacks safety equipment',
            'Other',

            'If other, please specify',
            'Do you have anything else you want to tell us?',
            'If yes, what is it?',
            'submission_time',
        ]

        submission_set1 = submission_set.filter(assessment__slug='pre_entrepreneurship')
        for line2 in submission_set1:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''

            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.id_number,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                get_choice_value(line2.data, 'can_plan_personal', 'rates'),
                get_choice_value(line2.data, 'can_plan_career', 'rates'),
                get_choice_value(line2.data, 'can_manage_financ', 'rates'),
                get_choice_value(line2.data, 'can_plan_time', 'rates'),
                get_choice_value(line2.data, 'can_suggest', 'rates'),
                get_choice_value(line2.data, 'can_take_decision', 'rates'),
                get_choice_value(line2.data, 'can_determin_probs', 'rates'),
                get_choice_value(line2.data, 'aware_resources', 'rates'),
                get_choice_value(line2.data, 'can_handle_pressure', 'rates'),
                get_choice_value(line2.data, 'motivated_advance_skills', 'rates'),

                get_choice_value(line2.data, 'communication_skills', 'skills'),
                get_choice_value(line2.data, 'presentation_skills', 'skills'),

                get_choice_value(line2.data, 'team_is', 'capacities'),
                get_choice_value(line2.data, 'good_team_is', 'capacities'),
                get_choice_value(line2.data, 'team_leader_is', 'capacities'),
                get_choice_value(line2.data, 'bad_decision_cause', 'capacities'),
                get_choice_value(line2.data, 'easiest_solution', 'capacities'),
                get_choice_value(line2.data, 'problem_solving', 'capacities'),

                submission_date,
            ]
            data5.append(content)

        submission_set2 = submission_set.filter(assessment__slug='post_entrepreneurship')
        for line2 in submission_set2:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.id_number,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                get_choice_value(line2.data, 'can_plan_personal', 'rates'),
                get_choice_value(line2.data, 'can_plan_career', 'rates'),
                get_choice_value(line2.data, 'can_manage_financ', 'rates'),
                get_choice_value(line2.data, 'can_plan_time', 'rates'),
                get_choice_value(line2.data, 'can_suggest', 'rates'),
                get_choice_value(line2.data, 'can_take_decision', 'rates'),
                get_choice_value(line2.data, 'can_determin_probs', 'rates'),
                get_choice_value(line2.data, 'aware_resources', 'rates'),
                get_choice_value(line2.data, 'can_handle_pressure', 'rates'),
                get_choice_value(line2.data, 'motivated_advance_skills', 'rates'),

                get_choice_value(line2.data, 'communication_skills', 'skills'),
                get_choice_value(line2.data, 'presentation_skills', 'skills'),

                get_choice_value(line2.data, 'team_is', 'capacities'),
                get_choice_value(line2.data, 'good_team_is', 'capacities'),
                get_choice_value(line2.data, 'team_leader_is', 'capacities'),
                get_choice_value(line2.data, 'bad_decision_cause', 'capacities'),
                get_choice_value(line2.data, 'easiest_solution', 'capacities'),
                get_choice_value(line2.data, 'problem_solving', 'capacities'),

                get_choice_value(line2.data, 'personal_value', 'rates'),
                get_choice_value(line2.data, 'faced_challenges', 'yes_no'),

                # get_choice_value(line2.data, 'challenges', 'challenges'),
                line2.data.get('challenges', ''),
                line2.get_data_option('challenges', 'difficult_material'),
                line2.get_data_option('challenges', 'no_support'),
                line2.get_data_option('challenges', 'too_short'),
                line2.get_data_option('challenges', 'too_long'),
                line2.get_data_option('challenges', 'inappropriate_venue'),

                # get_choice_value(line2.data, 'bad_venue', 'challenges'),
                line2.data.get('bad_venue', ''),
                line2.get_data_option('bad_venue', 'far'),
                line2.get_data_option('bad_venue', 'bad_ventilation'),
                line2.get_data_option('bad_venue', 'dirty_room'),
                line2.get_data_option('bad_venue', 'no_facility'),
                line2.get_data_option('bad_venue', 'no_tools'),
                line2.get_data_option('bad_venue', 'other'),

                line2.data.get('bad_venue_others', ''),
                get_choice_value(line2.data, 'has_comments', 'yes_no'),
                line2.data.get('additional_comments', ''),
                submission_date,
            ]
            data6.append(content)

        book.add_sheet(data5)
        book.add_sheet(data6)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_Entrepreneurship_Assessments.xls'
        return response


class ExportInitiativeAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.all()

    def get(self, request, *args, **kwargs):

        book = tablib.Databook()

        if self.request.user.is_superuser and not self.request.user.partner:
            submission_set = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        gov = self.request.GET.get('governorate', 0)
        if gov:
            submission_set = submission_set.filter(registration__governorate_id=int(gov))
        country = self.request.GET.get('country', 0)
        if country:
            submission_set = submission_set.filter(registration__partner_organization__locations=int(country))

        data5 = tablib.Dataset()
        data5.title = "Initiative registration"
        data5.headers = [
            'Country',
            'Governorate',
            'Location',
            'Partner',

            'Unique number',
            'First Name',
            "Father's Name",
            'Last Name',
            'Trainer',
            'Bayanati ID',
            'Jordanian ID',
            'Gender',
            'birthday day',
            'birthday month',
            'birthday year',
            'age',
            'Date of birth',
            'Nationality',
            'Marital status',
            'address',

            'Initiative Title',
            'Initiative Location',
            'Gender of members who were engaged in the initiative implementation',
            'Number of members who were engaged in the initiative implementation',
            'Planned start date of the initiative',
            'Duration of the initiative',

            'Type of Initiative',
            'basic services',
            'health service',
            'educational',
            'protection',
            'environmental',
            'political',
            'advocacy',
            'economic, artistic',
            'religious or spiritual',
            'sports',
            'social cohesion',
            'other',

            'Other initiatives',

            'How many people are estimated to benefit/will be reached by implementing the initiative?',
            '1-10 year old',
            '11-24 year old',
            '25-50 year old',
            '50 years and above',

            'The estimated Age groups of the beneficiaries?',
            'Gender of beneficiaries',
            'Did your group have a mentor/facilitator/teacher to support you with planning of the initiative?',
            'The team expects to implement the initiative as expected',
            'Team members expect to participate effectively in the implementation of the initiative',
            'The group aims to communicate with each other for the implementation of the initiative',
            'The group members expects to play leading roles for the implementation of the initiative',
            'The group expects to collect and analyse data for the implementation of the initiative',
            'The group expects to have a sense of belonging while implementing of the initiatives',
            'The group is confident in coming up with solutions if challenges are faced',
            'The group feels certain that the initiative will address the problem(s) faced by our communities',
            'The group expects to find the mentorship in the planning phase very helpful',
            'Are you planning to mobilize resources for this project?',

            'If yes, from whom?',
            'unicef',
            'Local business',
            'NGO',
            'Governmental body',
            'other',

            'What kind of support are you planning to receive?',
            'technical',
            'inkind',
            'financial',
            'other',

            'Can you tell us more about the problem you/your community is facing?',
            'Can you please tell us your planned results/what will the initiative achieve?',
            'start',
            'end',
            'submission time',
        ]

        data6 = tablib.Dataset()
        data6.title = "Initiative implementation"
        data6.headers = [
            'Country',
            'Governorate',
            'Location',
            'Partner',

            'Unique number',
            'First Name',
            "Father's Name",
            'Last Name',
            'Trainer',
            'Bayanati ID',
            'Jordanian ID',
            'Gender',
            'birthday day',
            'birthday month',
            'birthday year',
            'age',
            'Date of birth',
            'Nationality',
            'Marital status',
            'address',

            'Initiative Title',
            'Type of Initiative',
            'basic services',
            'health service',
            'educational',
            'protection',
            'environmental',
            'political',
            'advocacy',
            'economic, artistic',
            'religious or spiritual',
            'sports',
            'social cohesion',
            'other',

            'Other initiatives',
            'How many people benefited/ reached by implementing the initiative?',

            'The Age groups of the beneficiaries reached?',
            '1-10 year old',
            '11-24 year old',
            '25-49 year old',
            '50 years and above',
            'We don''t know',

            'Gender of beneficiaries',
            'The initiative was implemented as expected',

            'Types of challenges while implementing the initiative',
            'financial',
            'inkind',
            'physical',
            'technical',
            'other',
            'no_challenges',

            'Other challenges',

            'Team members participated effectively in the implementation of the initiative',
            'The group communicated with each other for the implementation of the initiative',
            'The group members played leading roles for the implementation of the initiative',
            'The group collected and analysed data for the implementation of the initiative',
            'The group had a sense of belonging while planning for the initiatives',
            'The group confidently came up with solutions when challenges were faced',
            'The group effectively addressed  the problem(s) faced by the community',
            'Did your group have a mentor/facilitator/teacher to support the implementation of the initiative',
            'The group found the mentorship in the planning phase very helpful',
            'Were resources mobilized for this project?',

            'If so, from whom?',
            'unicef',
            'Local business',
            'NGO',
            'Governmental body',
            'other',

            'What kind of support did you receive?',
            'technical',
            'inkind',
            'financial',
            'other',

            'The support we received was helpful and consistent with what the group was expecting',
            'If you answer is disagree or strongly disagree, can you tell us why?',
            'start',
            'end',
            'submission_time',
        ]

        submission_set1 = submission_set.filter(assessment__slug='init_registration')
        for line2 in submission_set1:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''

            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.id_number,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                line2.data.get('respid_initiativeID_title', ''),
                line2.data.get('initiative_loc', ''),
                get_choice_value(line2.data, 'gender_implem_initiatives', 'gender'),
                line2.data.get('No_of_team_members_executed', ''),
                line2.data.get('start_date_implementing_initia', ''),
                get_choice_value(line2.data, 'duration_of_initiative', 'how_many'),

                # get_choice_value(line2.data, 'type_of_initiative', 'initiative_types'),
                line2.data.get('type_of_initiative', ''),
                line2.get_data_option('type_of_initiative', 'basic_services'),
                line2.get_data_option('type_of_initiative', 'health_service'),
                line2.get_data_option('type_of_initiative', 'educational'),
                line2.get_data_option('type_of_initiative', 'protection'),
                line2.get_data_option('type_of_initiative', 'environmental'),
                line2.get_data_option('type_of_initiative', 'political'),
                line2.get_data_option('type_of_initiative', 'advocacy'),
                line2.get_data_option('type_of_initiative', 'economic_artis'),
                line2.get_data_option('type_of_initiative', 'religious_&_sp'),
                line2.get_data_option('type_of_initiative', 'sports'),
                line2.get_data_option('type_of_initiative', 'social_cohesio'),
                line2.get_data_option('type_of_initiative', 'other'),

                line2.get_data_option('other_type_of_initiative', ''),

                # get_choice_value(line2.data, 'number_of_direct_beneficiaries', 'how_many'),
                line2.data.get('number_of_direct_beneficiaries', ''),
                line2.get_data_option('number_of_direct_beneficiaries', '1-10'),
                line2.get_data_option('number_of_direct_beneficiaries', '11-24'),
                line2.get_data_option('number_of_direct_beneficiaries', '25-50'),
                line2.get_data_option('number_of_direct_beneficiaries', 'above_50'),

                get_choice_value(line2.data, 'age_group_range', 'how_many'),
                get_choice_value(line2.data, 'gender_of_beneficiaries', 'gender'),
                get_choice_value(line2.data, 'mentor_assigned', 'yes_no'),

                get_choice_value(line2.data, 'initiative_as_expected', 'rates'),
                get_choice_value(line2.data, 'team_involovement', 'rates'),
                get_choice_value(line2.data, 'communication', 'rates'),
                get_choice_value(line2.data, 'leadership', 'rates'),
                get_choice_value(line2.data, 'analytical_skills', 'rates'),
                get_choice_value(line2.data, 'sense_of_belonging', 'rates'),
                get_choice_value(line2.data, 'problem_solving', 'rates'),
                get_choice_value(line2.data, 'assertiveness', 'rates'),
                get_choice_value(line2.data, 'mentorship_helpful', 'rates'),

                get_choice_value(line2.data, 'planning_to_mobilize_resources', 'yes_no'),

                # get_choice_value(line2.data, 'if_so_who', 'third_parties'),
                line2.data.get('if_so_who', ''),
                line2.get_data_option('if_so_who', 'unicef'),
                line2.get_data_option('if_so_who', 'private,_local'),
                line2.get_data_option('if_so_who', 'NGO'),
                line2.get_data_option('if_so_who', 'Governmental_i'),
                line2.get_data_option('if_so_who', 'other'),

                # get_choice_value(line2.data, 'type_of_support_required', 'challenges'),
                line2.data.get('type_of_support_required', ''),
                line2.get_data_option('type_of_support_required', 'technical'),
                line2.get_data_option('type_of_support_required', 'inkind'),
                line2.get_data_option('type_of_support_required', 'financial'),
                line2.get_data_option('type_of_support_required', 'other'),

                line2.data.get('problem_addressed', ''),
                line2.data.get('planned_results', ''),
                line2.data.get('start', ''),
                line2.data.get('end', ''),

                submission_date,
            ]
            data5.append(content)

        submission_set2 = submission_set.filter(assessment__slug='init_exec')
        for line2 in submission_set2:
            youth = line2.youth
            registry = line2.registration
            submission_date = line2.data.get('_submission_time', '')
            try:
                submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                    '%d/%m/%Y') if submission_date else ''
            except Exception:
                submission_date = ''
            content = [
                registry.governorate.parent.name if registry.governorate else '',
                registry.governorate.name if registry.governorate else '',
                registry.location,
                registry.partner_organization.name if registry.partner_organization else '',

                youth.number,
                youth.first_name,
                youth.father_name,
                youth.last_name,
                registry.trainer,
                youth.bayanati_ID,
                youth.id_number,
                youth.sex,
                youth.birthday_day,
                youth.birthday_month,
                youth.birthday_year,
                youth.calc_age,
                youth.birthday,
                youth.nationality.name if youth.nationality else '',
                youth.marital_status,
                youth.address,

                line2.data.get('respid_initiativeID_title', ''),

                # get_choice_value(line2.data, 'type_of_initiative', 'initiative_types'),
                line2.data.get('type_of_initiative', ''),
                line2.get_data_option('type_of_initiative', 'basic_services'),
                line2.get_data_option('type_of_initiative', 'health_service'),
                line2.get_data_option('type_of_initiative', 'educational'),
                line2.get_data_option('type_of_initiative', 'protection'),
                line2.get_data_option('type_of_initiative', 'environmental'),
                line2.get_data_option('type_of_initiative', 'political'),
                line2.get_data_option('type_of_initiative', 'advocacy'),
                line2.get_data_option('type_of_initiative', 'economic_artis'),
                line2.get_data_option('type_of_initiative', 'religious_&_sp'),
                line2.get_data_option('type_of_initiative', 'sports'),
                line2.get_data_option('type_of_initiative', 'social_cohesio'),
                line2.get_data_option('type_of_initiative', 'other'),

                line2.data.get('other_type_of_initiative', ''),
                line2.data.get('integer_0259d46e', ''),

                # get_choice_value(line2.data, 'select_multiple_e160966a', 'how_many'), split the options
                line2.data.get('select_multiple_e160966a', ''),
                line2.get_data_option('select_multiple_e160966a', '1-10'),
                line2.get_data_option('select_multiple_e160966a', '11-24'),
                line2.get_data_option('select_multiple_e160966a', '25-49'),
                line2.get_data_option('select_multiple_e160966a', '50'),
                line2.get_data_option('select_multiple_e160966a', 'unknown'),

                get_choice_value(line2.data, 'select_one_a3c4ea99', 'gender'),
                get_choice_value(line2.data, 'initiative_as_expected', 'rates'),

                # get_choice_value(line2.data, 'challenges_faced', 'challenges'), split the options
                line2.data.get('challenges_faced', ''),
                line2.get_data_option('challenges_faced', 'financial'),
                line2.get_data_option('challenges_faced', 'inkind'),
                line2.get_data_option('challenges_faced', 'physical'),
                line2.get_data_option('challenges_faced', 'technical'),
                line2.get_data_option('challenges_faced', 'other'),
                line2.get_data_option('challenges_faced', 'no_challenges'),

                line2.data.get('other_challenges', ''),

                get_choice_value(line2.data, 'team_involovement', 'rates'),
                get_choice_value(line2.data, 'communication', 'rates'),
                get_choice_value(line2.data, 'leadership', 'rates'),
                get_choice_value(line2.data, 'analytical_skills', 'rates'),
                get_choice_value(line2.data, 'sense_of_belonging', 'rates'),
                get_choice_value(line2.data, 'problem_solving', 'rates'),
                get_choice_value(line2.data, 'assertiveness', 'rates'),

                get_choice_value(line2.data, 'mentor_assigned', 'yes_no'),
                get_choice_value(line2.data, 'mentorship_helpful', 'rates'),
                get_choice_value(line2.data, 'did_you_mobilize_resources', 'yes_no'),

                # get_choice_value(line2.data, 'mobilized_resources_through', 'third_parties'), split the options
                line2.data.get('mobilized_resources_through', ''),
                line2.get_data_option('mobilized_resources_through', 'unicef'),
                line2.get_data_option('mobilized_resources_through', 'private,_local'),
                line2.get_data_option('mobilized_resources_through', 'NGO'),
                line2.get_data_option('mobilized_resources_through', 'Governmental_i'),
                line2.get_data_option('mobilized_resources_through', 'other'),

                # get_choice_value(line2.data, 'type_of_support_required', 'challenges'), split the options
                line2.data.get('type_of_support_received', ''),
                line2.get_data_option('type_of_support_received', 'technical'),
                line2.get_data_option('type_of_support_received', 'inkind'),
                line2.get_data_option('type_of_support_received', 'financial'),
                line2.get_data_option('type_of_support_received', 'other'),

                get_choice_value(line2.data, 'support_received_helpful', 'rates'),
                line2.data.get('support_not_helpful_why', ''),
                line2.data.get('start', ''),
                line2.data.get('end', ''),

                submission_date,
            ]
            data6.append(content)

        book.add_sheet(data5)
        book.add_sheet(data6)

        response = HttpResponse(
            book.export("xls"),
            content_type='application/vnd.ms-excel',
        )
        response['Content-Disposition'] = 'attachment; filename=Beneficiary_Initiative_Assessments.xls'
        return response
