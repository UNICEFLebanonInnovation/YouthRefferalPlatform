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
            timestamp=time.time(),
            # title=registry.title,
            # location=registry.location,
            # type=registry.type,
        )

        url = '{form}?d[registry]={registry}&d[partner]={partner}&d[respid_initiativeID_title]={respid_initiativeID_title}&d[type_of_initiative]={type_of_initiative}&d[initiative_loc]={initiative_loc}' \
              '&returnURL={callback}'.format(
                form=assessment.assessment_form,
                registry=hashing.hashed,
                respid_initiativeID_title=registry.title,
                initiative_loc=registry.location,
                type_of_initiative=registry.type,
                partner=registry.partner_organization.name,
                # country=registry.governorate.parent.name,
                # nationality=youth.nationality.code,
                callback=self.request.META.get('HTTP_REFERER', registry.get_absolute_url())
        )
        return url

# # @method_decorator(csrf_exempt, name='dispatch')
# class YouthAssessmentSubmission(SingleObjectMixin, View):
#     def post(self, request, *args, **kwargs):
#
#         if 'registry' not in request.body:
#
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

# @method_decorator(csrf_exempt, name='dispatch')
# class YouthAssessmentSubmission(SingleObjectMixin, View):
#     def post(self, request, *args, **kwargs):
#         if 'registry' not in request.body:
#             return HttpResponseBadRequest()
#
#         payload = json.loads(request.body.decode('utf-8'))
#
#         hashing = AssessmentHash.objects.get(hashed=payload['registry'])
#         assessment = Assessment.objects.get(slug=hashing.assessment_slug)
#
#         if assessment.slug in ['init_registration', 'init_exec' ]:
#             from referral_platform.initiatives.models import YouthLedInitiative
#             registration = YouthLedInitiative.objects.get(id=int(hashing.registration))
#
#             submission, new = AssessmentSubmission.objects.get_or_create(
#                 initiative=registration,
#                 assessment=assessment,
#                 status='enrolled'
#             )
#         else:
#             registration = Registration.objects.get(id=int(hashing.registration))
#
#             submission, new = AssessmentSubmission.objects.get_or_create(
#                 registration=registration,
#                 youth=registration.youth,
#                 assessment=assessment,
#                 status='enrolled'
#             )
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
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(initiative__partner_organization=self.request.user.partner)

        return queryset

    def get(self, request, *args, **kwargs):

        headers = {

            'initiative__title': 'Initiative Title',
            'initiative__location__name': 'Initiative Location',
            'initiative__Participants__youth__first_name': 'First Name',
            'initiative__Participants__youth__last_name': 'Last Name',
            'initiative__type': 'Type of Initiative',
            'initiative__duration': 'Duration of the initiative',
            # 'initiative__knowledge_areas': 'Knowledge Areas',
            'assertiveness': 'The group feels certain that the initiative will address the problem(s) faced by our communities',
            'mentorship_helpful': 'The group expects to find the mentorship in the planning phase very helpful',
            'problem_addressed': 'Can you tell us more about the problem you/your community is facing?',
            'planned_results': 'Can you please tell us your planned results/what will the initiative achieve? ',
            'number_of_direct_beneficiaries':'How many people are estimated to benefit/will be reached by implementing the initiative?',
            'age_group_range': 'The estimated Age groups of the beneficiaries? ',
            'gender_of_beneficiaries': 'Gender of targeted beneficiaries',
            'mentor_assigned': 'Did your group have a mentor/facilitator/teacher to support you with planning of the initiative?',
            'initiative_as_expected': 'The team expects to implement the initiative as expected',
            'team_involovement': 'Team members expect to participate effectively in the implementation of the initiative',
            'communication': 'The group aims to communicate with each other for the implementation of the initiative',
            'leadership': 'The group members expects to play leading roles for the implementation of the initiative',
            'analytical_skills': 'The group expects to collect and analyse data for the implementation of the initiative',
            'sense_of_belonging': 'The group expects to have a sense of belonging while implementing of the initiatives',
            'problem_solving':'The group is confident in coming up with solutions if challenges are faced',
            'planning_to_mobilize_resources' : 'Are you planning to mobilize resources for this project?',
            'if_so_who': 'If yes, from whom?',
            'type_of_support_required': 'What kind of support are you planning to receive? ',

        }

        qs = self.get_queryset().extra(select={

            'assertiveness': "new_data->>'assertiveness'",
            'mentorship_helpful': "new_data->>'mentorship_helpful'",
            'problem_addressed': "new_data->>'problem_addressed'",
            'planned_results': "new_data->>'planned_results'",
            'number_of_direct_beneficiaries': "new_data->>'number_of_direct_beneficiaries'",
            'age_group_range': "new_data->>'age_group_range'",
            'gender_of_beneficiaries': "new_data->>'gender_of_beneficiaries'",
            'mentor_assigned': "new_data->>'mentor_assigned'",
            'initiative_as_expected': "new_data->>'initiative_as_expected'",
            'team_involovement': "new_data->>'team_involovement'",
            'communication': "new_data->>'communication'",
            'leadership': "new_data->>'leadership'",
            'analytical_skills': "new_data->>'analytical_skills'",
            'sense_of_belonging': "new_data->>'sense_of_belonging'",
            'problem_solving': "new_data->>'problem_solving'",

            'planning_to_mobilize_resources': "new_data->>'planning_to_mobilize_resources'",
            'if_so_who': "new_data->>'if_so_who'",
            'type_of_support_required': "new_data->>'type_of_support_required'",



        }).values(
            'initiative__title',
            'initiative__Participants__youth__last_name',
            'initiative__Participants__youth__first_name',
            'initiative__location__name',
            'initiative__type',
            'initiative__duration',
            'assertiveness',
            'mentorship_helpful',
            'problem_addressed',
            'planned_results',
            'number_of_direct_beneficiaries',
            'age_group_range',
            'gender_of_beneficiaries',
            'mentor_assigned',
            'initiative_as_expected',
            'team_involovement',
            'communication',
            'leadership',
            'analytical_skills',
            'sense_of_belonging',
            'problem_solving',
            'planning_to_mobilize_resources',
            'if_so_who',
            'type_of_support_required',



        )

        filename = 'Initiative-Export'

        return render_to_csv_response(qs, filename,  field_header_map=headers)
