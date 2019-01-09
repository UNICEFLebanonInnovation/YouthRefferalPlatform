from __future__ import absolute_import, unicode_literals

import json
import datetime
import time
from .tables import BootstrapTable, CommonTable, CommonTableAlt
from django.views.generic import ListView, FormView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.views.generic.edit import CreateView
from rest_framework import status
from rest_framework import viewsets, mixins, permissions
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin
from import_export.formats import base_formats
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import RedirectView
from django.shortcuts import render
from referral_platform.backends.djqscsv import render_to_csv_response
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from referral_platform.initiatives.models import AssessmentSubmission
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from referral_platform.registrations.models import Registration, Assessment, AssessmentHash


from referral_platform.users.views import UserRegisteredMixin

from .forms import YouthLedInitiativePlanningForm
from .models import YouthLedInitiative, YoungPerson


class YouthInitiativeView(LoginRequiredMixin, FilterView, SingleTableView):

    table_class = CommonTable
    model = YouthLedInitiative
    template_name = 'initiatives/list.html'
    table = BootstrapTable(YouthLedInitiative.objects.all(), order_by='id')

    def get_queryset(self):
        return YouthLedInitiative.objects.filter(partner_organization=self.request.user.partner)


class AddView(LoginRequiredMixin, FormView):

    template_name = 'initiatives/form.html'
    model = YouthLedInitiative
    success_url = '/initiatives/list.html'
    form_class = YouthLedInitiativePlanningForm
    form = YouthLedInitiativePlanningForm

    def get_form_class(self):
        form_class = YouthLedInitiativePlanningForm
        return form_class

    def get_success_url(self, ):
        # if self.request.POST.get('save_add_another', None):
        #     return '/initiatives/add/'
        # return self.success_url
        if self.request.POST.get('save_add_another', None):
            del self.request.session['instance_id']
            return '/initiatives/add/'
        if self.request.POST.get('save_and_continue', None):
            return '/initiatives/edit/' + str(self.request.session.get('instance_id')) + '/'
        return self.success_url

    def get_queryset(self):
        queryset = Registration.objects.filter(partner_organization=self.request.user.partner)
        return queryset

    def get_initial(self):
        # force_default_language(self.request, 'ar-ar')
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner_organization'] = self.request.user.partner_id
            # data['member'] = Registration.objects.filter(partner_organization=self.request.user.partner)
        initial = data
        return initial

    def form_valid(self, form):
        form.save(self.request)
        return super(AddView, self).form_valid(form)


class EditView(LoginRequiredMixin, FormView):
    template_name = 'initiatives/form.html'
    form_class = YouthLedInitiativePlanningForm
    model = YouthLedInitiative
    success_url = '/initiatives/list/'
    form = YouthLedInitiativePlanningForm

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(EditView, self).get_context_data(**kwargs)

    # def get_form_class(self):
    #     # if int(self.kwargs['term']) == 4:
    #     #     return GradingIncompleteForm
    #     return YouthLedInitiativePlanningForm

    def get_form(self, form_class=None):
        # form_class = self.get_form_class()
        form = YouthLedInitiativePlanningForm
        instance = YouthLedInitiative.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
        # print('instace is '+ instance)
        if self.request.method == "POST":
            return form(self.request.POST, instance=instance)
        else:
            return form(instance=instance)

    def form_valid(self, form):
        instance = YouthLedInitiative.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
        # self.fields['hidden_field'].initial = instance.id
        form.save(request=self.request, instance=instance)
        return super(EditView, self).form_valid(form)


class YouthAssessment(SingleObjectMixin, RedirectView):
    model = Assessment

    def get_redirect_url(self, *args, **kwargs):
        assessment = self.get_object()
        registry = YouthLedInitiative.objects.get(id=self.request.GET.get('registry'),
                                            partner_organization=self.request.user.partner_id)
        # youth = registry.youth
        hashing = AssessmentHash.objects.create(
            registration=registry.id,
            assessment_slug=assessment.slug,
            partner=self.request.user.partner_id,
            user=self.request.user.id,
            timestamp=time.time()
        )

        url = '{form}?d[registry]={registry}&d[partner]={partner}' \
              '&returnURL={callback}'.format(
                form=assessment.assessment_form,
                registry=hashing.hashed,

                partner=registry.partner_organization.name,
                # country=registry.governorate.parent.name,
                # nationality=youth.nationality.code,
                callback=self.request.META.get('HTTP_REFERER', registry.get_absolute_url())
        )
        return url


# # @method_decorator(csrf_exempt, name='dispatch')
# class YouthAssessmentSubmission(SingleObjectMixin, View):
#     def post(self, request, *args, **kwargs):
#         print('***********************fetet 3al submission**********************')
#         if 'registry' not in request.body:
#             print('***********************fetet 3al if **********************')
#             return HttpResponseBadRequest()
#
#         payload = json.loads(request.body.decode('utf-8'))
#
#         hashing = AssessmentHash.objects.get(hashed=payload['registry'])
#         # print('hash submission is ' + registry)
#         # print('hashion is ' + hashing.registration)
#         # assessment = Assessment.objects.get(slug=hashing.assessment_slug)
#         # submission, new = AssessmentSubmission.objects.get_or_create(
#         #     registration_id=int(hashing.registration),
#         #     assessment=assessment,
#         #     status='enrolled'
#         # )
#         #
#         # submission.data = payload
#         # submission.update_field()
#         # submission.save()
#         #
#         # return HttpResponse()
#         print('***********************fetet barra l if **********************)')
#         registration = YouthLedInitiative.objects.get(id=int(hashing.registration))
#         assessment = Assessment.objects.get(slug=hashing.assessment_slug)
#         print('***********************l hash hiye********************** ' + hashing.registration)
#         submission, new = AssessmentSubmission.objects.get_or_create(
#             registration=registration,
#             youth=registration.youth,
#             assessment=assessment,
#             status='enrolled'
#         )
#         submission.data = payload
#         submission.update_field()
#         submission.save()
#
#         return HttpResponse()

class ExportInitiativeAssessmentsView(LoginRequiredMixin, ListView):

    model = AssessmentSubmission
    queryset = AssessmentSubmission.objects.filter(assessment__slug__in=['init_exec', 'init_registration'])

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.queryset.filter(
                initiative__location__parent__name_en=self.request.user.country.name_en)
        else:
            queryset = self.queryset.filter(initiative__partner_organization=self.request.user.partner)

        return queryset

    def get(self, request, *args, **kwargs):

        headers = {

            'respid_initiativeID_title': 'Initiative Title',
            'initiative_loc': 'Initiative Location',
            'gender_implem_initiatives': 'Gender of members who were engaged in the initiative implementation',
            'No_of_team_members_executed': 'Number of people engaged in the initiative implementation',
            # 'integer_0259d46e': 'How many people benefited/ reached by implementing the initiative?',
            'start_date_implementing_initia': 'Planned start date of the initiative',
            'type_of_initiative': 'Type of Initiative',
            'other_type_of_initiative': 'If other, please specify',
            'duration_of_initiative': 'Duration of the initiative',
            # 'select_multiple_e160966a': 'The Age groups of the beneficiaries reached?',
            # 'select_one_a3c4ea99': 'Sex of beneficiaries',
            'leadership': 'The group members expects to play leading roles for the implementation of the initiative ',
            'challenges_faced': 'Types of challenges while implementing the initiative',
            'other_challenges': 'Others, please specify',
            'number_of_direct_beneficiaries': 'How many people are estimated to benefit/will be reached by implementing the initiative?',
            'age_group_range': 'The estimated Age groups of the beneficiaries?',
            'gender_of_beneficiaries': 'Gender of beneficiaries',
            'mentor_assigned': 'Did your group have a mentor/facilitator/teacher to support you with planning of the initiative?',
            'initiative_as_expected': 'The team expects to implement the initiative as expected',
            'team_involovement': 'Team members expect to participate effectively in the implementation of the initiative',
            'communication': 'The group aims to communicate with each other for the implementation of the initiative',
            #'analytical_skills': 'The group expects to collect and analyse data for the implementation of the initiative ',
            'analytical_skills': 'The group expects to collect and analyse data for the implementation of the initiative',
            'sense_of_belonging': 'The group expects to have a sense of belonging while implementing of the initiatives',
            'problem_solving': 'The group is confident in coming up with solutions if challenges are faced',
            'assertiveness': 'The group feels certain that the initiative will address the problem(s) faced by our communities',
            'mentorship_helpful': 'The group expects to find the mentorship in the planning phase very helpful',
            'problem_addressed': 'Can you tell us more about the problem you/your community is facing?',
            'planned_results': 'Can you please tell us your planned results/what will the initiative achieve? ',
            'planning_to_mobilize_resources': 'Are you planning to mobilize resources for this project?',
            'mobilized_resources_through': 'If so, from whom?',
            'did_you_mobilize_resources': 'Were resources mobilized for this project?',
            '_geolocation': 'Location',
            'if_so_who': 'If yes, from whom?',

            'type_of_support_required': 'What kind of support are you planning to receive?',
            'type_of_support_received': 'What kind of support did you receive?',
            'support_received_helpful': 'The support we received was helpful and consistent with what the group was expecting',
            'support_not_helpful_why': 'If you answer is disagree or strongly disagree, can you tell us why?',

            'start': 'Start Date',
            'end': 'End ',
            '_submission_time': 'submission time',
            '_userform_id': 'Registered by',
        }

        qs = self.get_queryset().extra(select={

            'respid_initiativeID_title': "new_data->>'respid_initiativeID_title'",
            'initiative_loc': "new_data->>'initiative_loc'",
            'gender_implem_initiatives': "new_data->>'gender_implem_initiatives'",
            'No_of_team_members_executed': "new_data->>'No_of_team_members_executed'",
            # 'integer_0259d46e': "new_data->>'integer_0259d46e'",
            'start_date_implementing_initia': "new_data->>'start_date_implementing_initia'",
            'type_of_initiative': "new_data->>'type_of_initiative'",
            'other_type_of_initiative': "new_data->>'other_type_of_initiative'",
            'duration_of_initiative': "new_data->>'duration_of_initiative'",
            # 'select_multiple_e160966a': "new_data->>'select_multiple_e160966a'",
            # 'select_one_a3c4ea99': "new_data->>'select_one_a3c4ea99'",
            'leadership': "new_data->>'leadership'",
            'challenges_faced': "new_data->>'challenges_faced'",
            'other_challenges': "new_data->>'other_challenges'",
            'number_of_direct_beneficiaries': "new_data->>'number_of_direct_beneficiaries'",
            'age_group_range': "new_data->>'age_group_range'",
            'gender_of_beneficiaries': "new_data->>'gender_of_beneficiaries'",
            'mentor_assigned': "new_data->>'mentor_assigned'",
            'initiative_as_expected': "new_data->>'initiative_as_expected'",
            'team_involovement': "new_data->>'team_involovement'",
            'communication': "new_data->>'communication'",
            'problem_solving': "new_data->>'problem_solving'",
            'analytical_skills': "new_data->>'analytical_skills'",
            'sense_of_belonging': "new_data->>'sense_of_belonging'",
            'assertiveness': "new_data->>'assertiveness'",
            'mentorship_helpful': "new_data->>'mentorship_helpful'",
            'problem_addressed': "new_data->>'problem_addressed'",
            'planned_results': "new_data->>'planned_results'",
            'planning_to_mobilize_resources': "new_data->>'planning_to_mobilize_resources'",
            'mobilized_resources_through': "new_data->>'mobilized_resources_through'",
            'did_you_mobilize_resources': "new_data->>'did_you_mobilize_resources'",
            '_geolocation': "new_data->>'_geolocation'",
            'if_so_who': "new_data->>'if_so_who'",

            'type_of_support_required': "new_data->>'type_of_support_required'",
            'type_of_support_received': "new_data->>'type_of_support_received'",
            'support_received_helpful': "new_data->>'support_received_helpful'",
            'support_not_helpful_why': "new_data->>'support_not_helpful_why'",

            'start': "new_data->>'start'",
            'end': "new_data->>'end'",
            '_submission_time': "new_data->>'_submission_time'",
            '_userform_id': "new_data->>'_userform_id'",

        }).values(
            'registration__youth__first_name',
            'registration__youth__father_name',
            'registration__youth__last_name',
            'registration__partner_organization__name',
            'registration__youth__bayanati_ID',
            'registration__youth__birthday_day',
            'registration__youth__birthday_month',
            'registration__youth__birthday_year',
            'registration__youth__nationality__code',
            'registration__youth__marital_status',
            'registration__youth__sex',
            'registration__youth__number',
            'registration__governorate__parent__name_en',
            'registration__governorate__name_en',
            'registration__center__name',
            'registration__location',
            'assessment__overview',

            'respid_initiativeID_title',
            'initiative_loc',
            'gender_implem_initiatives',
            'No_of_team_members_executed',
            # 'integer_0259d46e',
            'start_date_implementing_initia',
            'type_of_initiative',
            'other_type_of_initiative',
            'duration_of_initiative',
            # 'select_multiple_e160966a',
            # 'select_one_a3c4ea99',
            'leadership',
            'challenges_faced',
            'other_challenges',
            'number_of_direct_beneficiaries',
            'age_group_range',
            'gender_of_beneficiaries',
            'mentor_assigned',
            'initiative_as_expected',
            'team_involovement',
            'communication',
            #'analytical_skills',
            'analytical_skills',
            'sense_of_belonging',
            'problem_solving',
            'assertiveness',
            'mentorship_helpful',
            'problem_addressed',
            'planned_results',
            'planning_to_mobilize_resources',
            'mobilized_resources_through',
            'did_you_mobilize_resources',
            '_geolocation',
            'if_so_who',

            'type_of_support_required',
            'type_of_support_received',
            'support_received_helpful',
            'support_not_helpful_why',

            'start',
            'end',
            '_submission_time',
            '_userform_id',
        )

        filename = 'Initiative-Export'

        return render_to_csv_response(qs, filename,  field_header_map=headers)
