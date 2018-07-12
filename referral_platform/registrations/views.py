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

        return queryset

    def get(self, request, *args, **kwargs):

        headers = {
            # 'country': 'Country',
            'governorate__parent__name': 'Country',
            'governorate__name': 'Governorate',
            'partner_organization__name': 'Partner',
            'center__name': 'Center',
            'location': 'Location',
            'youth__first_name': 'First Name',
            'youth__father_name': "Father's Name",
            'youth__last_name': 'Last Name',
            'trainer': 'Trainer',
            'youth__bayanati_ID': 'Bayanati ID',
            'youth__sex': 'Gender',
            'youth__birthday_day': 'birthday day',
            'youth__birthday_month': 'birthday month',
            'youth__birthday_year': 'birthday year',
            'registration__youth_age': 'Age',
            'youth__nationality__name': 'Nationality',
            'youth__marital_status': 'Marital status',
            'youth__address': 'address',
            'owner__email': 'Created By',
            'modified_by__email': 'modified_by',
            'created': 'created',
            'modified': 'modified',
    }
        qs = self.get_queryset().values(
            'youth__first_name',
            'youth__father_name',
            'youth__last_name',
            'trainer',
            'youth__bayanati_ID',
            'youth__sex',
            'youth__birthday_day',
            'youth__birthday_month',
            'youth__birthday_year',
            'location',
            'governorate__name',
            'governorate__parent__name',
            'partner_organization__name',
            'center__name',
            'youth__nationality__name',
            'youth__marital_status',
            'youth__address',
            'owner__email',
            'modified_by__email',
            'created',
            'modified',
            'registration__youth_age',
        )
        filename = 'beneficiaries'

        return render_to_csv_response(qs, filename, field_header_map=headers)


class ExportRegistryAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.filter(assessment__slug='registration')

    def get_queryset(self):
        if self.request.user.is_superuser and not self.request.user.partner:
            queryset = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        return self.queryset

    def get(self, request, *args, **kwargs):

        headers = {
            'registration__youth__first_name': 'First Name',
            'registration__youth__father_name': "Fathers's Name",
            'registration__youth__last_name': 'Last Name',
            'registration__youth__bayanati_ID': 'Bayanati ID',
            'registration__youth__birthday_day': 'Birth Day',
            'registration__youth__birthday_month': 'Birth Month',
            'registration__youth__birthday_year': 'Birth Year',
            'registration__youth__nationality__name': 'Nationality',
            'registration__youth__marital_status': 'Marital status',
            'registration__youth__sex': 'Gender',
            'registration__governorate__parent__name': 'Country',
            'registration__governorate__name': 'Governorate',
            'registration__center__name': 'Center',
            'registration__location': 'Location',
            # 'nationality': 'Nationality',
            # 'training_type': 'Training Type',
            # 'partner': 'Partner Organization',
            'center_type': 'Center Type',
            'occupation_type': 'Occupation Type',
            'educational_status': 'Educational Status',
            'School_name': 'School name',
            'School_type': 'Type of school',
            'school_level': 'School Level',
            'reason_for_skipping_class': 'Reason fro skipping Classes',
            'family_present': 'Family composition',
            'not_present_where': 'Reason of family absence',
            'family_not_present': 'TBD',
            'Accommodation_type': 'Accommodation Type',
            'how_many_times_skipped_school': 'How many times have you missed your classes in the past 3 months ',
            'drugs_substance_use': 'Any family member use drug/alcohol?',
            'how_many_times_displaced': 'Displacement status',
            'Relation_with_labor_market': 'Relationship with Labour Market',
            'reasons_for_not_feeling_safe_a': 'Reasons for not feeling safe most or all of the time',
            'feeling_of_safety_security': 'Feeling of safety',
            'concent_paper': 'Conscent form filled',
            'family_steady_income': 'Family Income',
            'training_date': 'Training Date',
            'training_end_date': 'Training End Date',
            '_submission_time': 'Submission Time and Date',
            'what_electronics_do_you_own': 'What electronics do you own?',
            'desired_method_for_follow_up': 'Desired Method for follow-up',

         }

        qs = self.get_queryset().extra(select={
            # 'partner': "data->>'partner'",
            'educational_status': "data->>'educational_status'",
            # 'country': "data->>'country'",
            # 'nationality': "data->>'nationality'",
            # 'training_type': "data->>'training_type'",

            # 'phonenumber': "data->>'phonenumber'",

            'center_type': "data->>'center_type'",
            'occupation_type': "data->>'occupation_type'",
            'School_name': "data->>'School_name'",
            'School_type': "data->>'School_type'",
            'school_level': "data->>'School_level'",
            'reason_for_skipping_class': "data->>'reason_for_skipping_class'",
            'family_present': "data->>'family_present'",
            'family_not_present': "data->>'family_not_present'",
            'not_present_where': "data->>'not_present_where'",
            'Accommodation_type': "data->>'Accommodation_type'",
            'how_many_times_skipped_school': "data->>'how_many_times_skipped_school'",
            'drugs_substance_use': "data->>'drugs_substance_use'",
            'how_many_times_displaced': "data->>'how_many_times_displaced'",
            'Relation_with_labor_market': "data->>'Relation_with_labor_market'",
            'reasons_for_not_feeling_safe_a': "data->>'reasons_for_not_feeling_safe_a'",
            'feeling_of_safety_security': "data->>'feeling_of_safety_security'",
            'concent_paper': "data->>'concent_paper'",
            'family_steady_income': "data->>'family_steady_income'",
            'training_date': "data->>'training_date'",
            'training_end_date': "data->>'training_end_date'",
            '_submission_time': "data->>'_submission_time'",
            'what_electronics_do_you_own': "data->>'what_electronics_do_you_own'",
            'desired_method_for_follow_up': "data->>'desired_method_for_follow_up'",

            # 'youth_fname':"registration->>youth__last_name",
            # 'youth_lname':"registration->>youth__first_name",

        }).values(
            'registration__youth__first_name',
            'registration__youth__father_name',
            'registration__youth__last_name',
            # 'partner',
            'educational_status',
            # 'country',
            # 'nationality',
            # 'training_type',
            'registration__governorate__parent__name',
            'registration__governorate__name',
            'registration__center__name',
            'registration__location',
            'registration__youth__bayanati_ID',
            'registration__youth__birthday_day',
            'registration__youth__birthday_month',
            'registration__youth__birthday_year',
            'registration__youth__nationality__name',
            'registration__youth__marital_status',
            'registration__youth__sex',
            'center_type',
            'occupation_type',
            'School_name',
            'School_type',
            'school_level',
            'reason_for_skipping_class',
            'family_present',
            'family_not_present',
            'not_present_where',
            'Accommodation_type',
            'how_many_times_skipped_school',
            'drugs_substance_use',
            'how_many_times_displaced',
            'Relation_with_labor_market',
            'reasons_for_not_feeling_safe_a',
            'feeling_of_safety_security',
            'concent_paper',
            'family_steady_income',
            'training_date',
            'training_end_date',
            '_submission_time',
            'what_electronics_do_you_own',
            'desired_method_for_follow_up',
        )
        filename = 'registrations'

        return render_to_csv_response(qs, filename, field_header_map=headers)


class ExportCivicAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.filter(assessment__slug__in=['pre_assessment', 'post_assessment'])

    def get_queryset(self):
        if self.request.user.is_superuser and not self.request.user.partner:
            queryset = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        return self.queryset

    def get(self, request, *args, **kwargs):

        headers = {
            'registration__youth__first_name': 'First Name',
            'registration__youth__father_name': "Fathers's Name",
            'registration__youth__last_name': 'Last Name',
            'registration__youth__bayanati_ID': 'Bayanati ID',
            'registration__youth__birthday_day': 'Birth Day',
            'registration__youth__birthday_month': 'Birth Month',
            'registration__youth__birthday_year': 'Birth Year',
            'registration__youth__nationality__name': 'Nationality',
            'registration__youth__marital_status': 'Marital status',
            'registration__youth__sex': 'Gender',
            'registration__governorate__parent__name': 'Country',
            'registration__governorate__name': 'Governorate',
            'registration__center__name': 'Center',
            'registration__location': 'Location',
            'assessment__slug': 'Assessment Type',
            # 'nationality': 'Nationality',
            # 'training_type': 'Training Type',
            # 'partner': 'Partner Organization',

            '_4_articulate_thoughts': 'I can articulate/state my thoughts, feelings and ideas to others well',
            '_1_express_opinion': 'I can express my opinions when my classmates/friends/peers disagree with me',
            '_20_discussions_with_peers_before_': 'Usually I discuss with others before making decisions',
            '_28_discuss_opinions': 'I build on the ideas of others.',
            '_31_willing_to_compromise': 'I am willing to compromise my own view to obtain a group consensus.',
            '_pal_I_belong': 'I feel I belong to my community',
            '_41_where_to_volunteer': 'I know where to volunteer in my community',
            '_42_regularly_volunteer': 'I volunteer on a regular basis in my community',
            '_pal_contrib_appreciated': 'I feel I am appreciated for my contributions to my community.',
            '_pal_contribute_to_development': 'I believe I can contribute towards community development',
            '_51_communicate_community_conc': 'I am able to address community concerns with community leaders',
            '_52_participate_community_medi': 'I participate in addressing my community concerns through SMedia',
            '_submission_time': 'Submission time',
        }

        qs = self.get_queryset().extra(select={
            '_4_articulate_thoughts': "data->>'_4_articulate_thoughts'",
            '_1_express_opinion': "data->>'_1_express_opinion'",
            '_20_discussions_with_peers_before_': "data->>'_20_discussions_with_peers_before_'",
            '_28_discuss_opinions': "data->>'_28_discuss_opinions'",
            '_31_willing_to_compromise': "data->>'_31_willing_to_compromise'",
            '_pal_I_belong': "data->>'_pal_I_belong'",
            '_41_where_to_volunteer': "data->>'_41_where_to_volunteer'",
            '_42_regularly_volunteer': "data->>'_42_regularly_volunteer'",
            '_pal_contrib_appreciated': "data->>'_pal_contrib_appreciated'",
            '_pal_contribute_to_development': "data->>'_pal_contribute_to_development'",
            '_51_communicate_community_conc': "data->>'_51_communicate_community_conc'",
            '_52_participate_community_medi': "data->>'_52_participate_community_medi'",
            '_submission_time': "data->>'_submission_time'",


        }).values(
            'registration__youth__first_name',
            'registration__youth__father_name',
            'registration__youth__last_name',
            'registration__governorate__parent__name',
            'registration__governorate__name',
            'registration__center__name',
            'registration__location',
            'registration__youth__bayanati_ID',
            'registration__youth__birthday_day',
            'registration__youth__birthday_month',
            'registration__youth__birthday_year',
            'registration__youth__nationality__name',
            'registration__youth__marital_status',
            'registration__youth__sex',
            'assessment__slug',
            '_4_articulate_thoughts',
            '_1_express_opinion',
            '_20_discussions_with_peers_before_',
            '_28_discuss_opinions',
            '_31_willing_to_compromise',
            '_pal_I_belong',
            '_41_where_to_volunteer',
            '_42_regularly_volunteer',
            '_pal_contrib_appreciated',
            '_pal_contribute_to_development',
            '_51_communicate_community_conc',
            '_52_participate_community_medi',
            '_submission_time',

        )
        filename = 'Civic-assessment'

        return render_to_csv_response(qs, filename, field_header_map=headers)


class ExportEntrepreneurshipAssessmentsView(LoginRequiredMixin, ListView):
    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.filter(assessment__slug__in=['pre_entrepreneurship', 'post_entrepreneurship'])

    def get_queryset(self):
        if self.request.user.is_superuser and not self.request.user.partner:
            queryset = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        return self.queryset

    def get(self, request, *args, **kwargs):

        headers = {
            'registration__youth__first_name': 'First Name',
            'registration__youth__father_name': "Fathers's Name",
            'registration__youth__last_name': 'Last Name',
            'registration__youth__bayanati_ID': 'Bayanati ID',
            'registration__youth__birthday_day': 'Birth Day',
            'registration__youth__birthday_month': 'Birth Month',
            'registration__youth__birthday_year': 'Birth Year',
            'registration__youth__nationality__name': 'Nationality',
            'registration__youth__marital_status': 'Marital status',
            'registration__youth__sex': 'Gender',
            'registration__governorate__parent__name': 'Country',
            'registration__governorate__name': 'Governorate',
            'registration__center__name': 'Center',
            'registration__location': 'Location',
            'assessment__slug': 'Assessment Type',
            # 'nationality': 'Nationality',
            # 'training_type': 'Training Type',
            # 'partner': 'Partner Organization',

            'can_plan_personal': 'I am prepared to plan my personal objectives',
            'can_plan_career': 'I am prepared to plan my professional objectives',
            'can_manage_financ': 'I know how to manage my monetary affairs responsibly',
            'can_plan_time': 'I know ways to plan my time',
            'can_suggest': 'I can give suggestions without being bossy',
            'can_take_decision': 'I make a decision by thinking about all the information I have about available options decision making',
            'problem_solving': 'I know how to identify causes for my problems and find solutions for them  problem solving',
            'aware_resources': 'I know where and when to get support when I face a problem',
            'can_handle_pressure': 'When I am stressed, I manage my stress in a positive way',
            'motivated_advance_skills': 'There are opportunities in the labour market that encourage me to develop my skills',

            'communication_skills': 'A good communicator',
            'presentation_skills': 'The most important part of delivering a successful presentation is',

            'team_is': 'A team is a group of people who',
            'good_team_is': 'To work efficiently as a team',
            'team_leader_is': 'If I am the group leader, I will',
            'bad_decision_cause': 'One of the main reasons to NOT make the best decision',
            'easiest_solution': 'The easiest solution for the problem is always the best solution',
            'can_determin_probs': 'If you face a problem, what procedures would you take into consideration to solve the problem? Please arrange the below steps chronologically',
            '_submission_time': 'submission time',

            'personal_value': 'Rate the benefits of the training to your personal life',
            'faced_challenges': 'Have you faced any challenges with the program?',
            'challenges': 'Challenges',
            'has_comments': 'Comments',
            '_userform_id': 'User',

        }

        qs = self.get_queryset().extra(select={

            'can_plan_personal': "data->>'can_plan_personal'",
            'can_plan_career': "data->>'can_plan_career'",
            'can_manage_financ': "data->>'can_manage_financ'",
            'can_plan_time': "data->>'can_plan_time'",
            'can_suggest': "data->>'can_suggest'",
            'can_take_decision': "data->>'can_take_decision'",
            'problem_solving': "data->>'problem_solving'",
            'aware_resources': "data->>'aware_resources'",
            'can_handle_pressure': "data->>'can_handle_pressure'",
            'motivated_advance_skills': "data->>'motivated_advance_skills'",

            'communication_skills': "data->>'communication_skills'",
            'presentation_skills': "data->>'presentation_skills'",

            'team_is': "data->>'team_is'",
            'good_team_is': "data->>'good_team_is'",
            'team_leader_is': "data->>'team_leader_is'",
            'bad_decision_cause': "data->>'bad_decision_cause'",
            'easiest_solution': "data->>'easiest_solution'",
            'can_determin_probs': "data->>'can_determin_probs'",
            '_submission_time': "data->>'_submission_time'",

            'personal_value': "data->>'personal_value'",
            'faced_challenges': "data->>'faced_challenges'",
            'challenges': "data->>'challenges'",
            'has_comments': "data->>'has_comments'",
            '_userform_id': "data->>'_userform_id'",

        }).values(
            'registration__youth__first_name',
            'registration__youth__father_name',
            'registration__youth__last_name',
            'registration__governorate__parent__name',
            'registration__governorate__name',
            'registration__center__name',
            'registration__location',
            'registration__youth__bayanati_ID',
            'registration__youth__birthday_day',
            'registration__youth__birthday_month',
            'registration__youth__birthday_year',
            'registration__youth__nationality__name',
            'registration__youth__marital_status',
            'registration__youth__sex',
            'assessment__slug',
             'can_plan_personal',
            'can_plan_career',
            'can_manage_financ',
            'can_plan_time',
            'can_suggest',
            'can_take_decision',
            'problem_solving',
            'aware_resources',
            'can_handle_pressure',
            'motivated_advance_skills',

            'communication_skills',
            'presentation_skills',

            'team_is',
            'good_team_is',
            'team_leader_is',
            'bad_decision_cause',
            'easiest_solution',
            'can_determin_probs',
            '_submission_time',

            'personal_value',
            'faced_challenges',
            'challenges',
            'has_comments',
            '_userform_id',

        )
        filename = 'Entrepreneurship-assessment'

        return render_to_csv_response(qs, filename, field_header_map=headers)


            # 'If the room/ training area not convenient, please specify why',
            # 'Location of CBO is too far',
            # 'The rooms are not very well ventilated',
            # 'The rooms are not clean',
            # 'There are no tables / chairs',
            # 'The classroom lacks safety equipment',
            # 'Other',
            #
            # 'If other, please specify',
            # 'Do you have anything else you want to tell us?',
            # 'If yes, what is it?',
            # 'submission_time',


class ExportInitiativeAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.filter(assessment__slug__in=['init_exec', 'init_registration'])

    def get_queryset(self):
        if self.request.user.is_superuser and not self.request.user.partner:
            queryset = self.queryset
        else:
            submission_set = self.queryset.filter(registration__partner_organization=self.request.user.partner)

        return self.queryset

    def get(self, request, *args, **kwargs):

        headers = {
            'registration__youth__first_name': 'First Name',
            'registration__youth__father_name': "Fathers's Name",
            'registration__youth__last_name': 'Last Name',
            'registration__youth__bayanati_ID': 'Bayanati ID',
            'registration__youth__birthday_day': 'Birth Day',
            'registration__youth__birthday_month': 'Birth Month',
            'registration__youth__birthday_year': 'Birth Year',
            'registration__youth__nationality__name': 'Nationality',
            'registration__youth__marital_status': 'Marital status',
            'registration__youth__sex': 'Gender',
            'registration__governorate__parent__name': 'Country',
            'registration__governorate__name': 'Governorate',
            'registration__center__name': 'Center',
            'registration__location': 'Location',
            'assessment__slug': 'Assessment Type',

            'respid_initiativeID_title': 'Initiative Title',
            'initiative_loc': 'Initiative Location',
            'gender_implem_initiatives': 'Gender of members who were engaged in the initiative implementation',
            'No_of_team_members_executed': 'Number of people engaged in the initiative implementation',
            'start_date_implementing_initia': 'Planned start date of the initiative',
            'duration_of_initiative': 'Duration of the initiative',
            '_tags': 'Initiative Tags',
            'type_of_initiative': 'Type of Initiative',
            'basic_services': 'basic services',

            'number_of_direct_beneficiaries': 'How many people are estimated to benefit/will be reached by implementing the initiative?',
            'age_group_range': 'The estimated Age groups of the beneficiaries?',
            'gender_of_beneficiaries': 'Gender of beneficiaries',
            'mentor_assigned': 'Did your group have a mentor/facilitator/teacher to support you with planning of the initiative?',
            'planned_results': 'The team expects to implement the initiative as expected',
            'team_involovement': 'Team members expect to participate effectively in the implementation of the initiative',
            'communication': 'The group aims to communicate with each other for the implementation of the initiative',
            #'sense_of_belonging': 'The group members expects to play leading roles for the implementation of the initiative',
            'analytical_skills': 'The group expects to collect and analyse data for the implementation of the initiative',
            'sense_of_belonging': 'The group expects to have a sense of belonging while implementing of the initiatives',
            'assertiveness': 'The group is confident in coming up with solutions if challenges are faced',
            'problem_solving': 'The group feels certain that the initiative will address the problem(s) faced by our communities',
            'mentorship_helpful': 'The group expects to find the mentorship in the planning phase very helpful',
            'planning_to_mobilize_resources': 'Are you planning to mobilize resources for this project?',
            '_geolocation': 'Location',
            'if_so_who': 'If yes, from whom?',

            'type_of_support_required': 'What kind of support are you planning to receive?',

            'problem_addressed': 'Can you tell us more about the problem you/your community is facing?',
            'initiative_as_expected': 'Can you please tell us your planned results/what will the initiative achieve?',
            'start': 'Start Date',
            'end': 'End ',
            '_submission_time': 'submission time',
            '_userform_id': 'Registered by',
        }

        qs = self.get_queryset().extra(select={

            'respid_initiativeID_title': "data->>'respid_initiativeID_title'",
            'initiative_loc': "data->>'initiative_loc'",
            'No_of_team_members_executed': "data->>'No_of_team_members_executed'",
            'start_date_implementing_initia': "data->>'start_date_implementing_initia'",
            'duration_of_initiative': "data->>'duration_of_initiative'",
            '_tags': "data->>'_tags'",
            'type_of_initiative': "data->>'type_of_initiative'",
            'basic_services': "data->>'basic_services'",

            'number_of_direct_beneficiaries': "data->>'number_of_direct_beneficiaries'",
            'age_group_range': "data->>'age_group_range'",
            'gender_of_beneficiaries': "data->>'gender_of_beneficiaries'",
            'mentor_assigned': "data->>'mentor_assigned'",
            'planned_results': "data->>'planned_results'",
            'team_involovement': "data->>'team_involovement'",
            'communication': "data->>'communication'",
            #'sense_of_belonging': 'The group members expects to play leading roles for the implementation of the initiative',
            'analytical_skills': "data->>'analytical_skills'",
            'sense_of_belonging': "data->>'sense_of_belonging'",
            'assertiveness': "data->>'assertiveness'",
            'problem_solving': "data->>'problem_solving'",
            'mentorship_helpful': "data->>'mentorship_helpful'",
            'planning_to_mobilize_resources': "data->>'planning_to_mobilize_resources'",
            'gender_implem_initiatives': "data->>'gender_implem_initiatives'",
            '_geolocation': "data->>'_geolocation'",
            'if_so_who': "data->>'if_so_who'",

            'type_of_support_required': "data->>'type_of_support_required'",

            'problem_addressed': "data->>'problem_addressed'",
            'initiative_as_expected': "data->>'initiative_as_expected'",
            'start': "data->>'start'",
            'end': "data->>'end'",
            '_submission_time': "data->>'_submission_time'",
            '_userform_id': "data->>'_userform_id'",

        }).values(
            'registration__youth__first_name',
            'registration__youth__father_name',
            'registration__youth__last_name',
            'registration__governorate__parent__name',
            'registration__governorate__name',
            'registration__center__name',
            'registration__location',
            'registration__youth__bayanati_ID',
            'registration__youth__birthday_day',
            'registration__youth__birthday_month',
            'registration__youth__birthday_year',
            'registration__youth__nationality__name',
            'registration__youth__marital_status',
            'registration__youth__sex',
            'assessment__slug',


            'respid_initiativeID_title',
            'initiative_loc',
            'No_of_team_members_executed',
            'start_date_implementing_initia',
            'duration_of_initiative',
            '_tags',
            'type_of_initiative',
            'basic_services',

            'number_of_direct_beneficiaries',
            'age_group_range',
            'gender_of_beneficiaries',
            'mentor_assigned',
            'planned_results',
            'team_involovement',
            'communication',
            #'sense_of_belonging': 'The group members expects to play leading roles for the implementation of the initiative',
            'analytical_skills',
            'sense_of_belonging',
            'assertiveness',
            'problem_solving',
            'mentorship_helpful',
            'planning_to_mobilize_resources',
            'gender_implem_initiatives',
            '_geolocation',
            'if_so_who',

            'type_of_support_required',

            'problem_addressed',
            'initiative_as_expected',
            'start',
            'end',
            '_submission_time',
            '_userform_id',

        )
        filename = 'Initiative-Export'

        return render_to_csv_response(qs, filename,  field_header_map=headers)
