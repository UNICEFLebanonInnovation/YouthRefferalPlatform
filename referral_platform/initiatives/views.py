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
            title=registry.title,
            location=registry.location,
            type=registry.type,
        )

        url = '{form}?d[registry]={registry}&d[partner]={partner}&d[title]={title}&d[location]={location}&d[type]={type}' \
              '&returnURL={callback}'.format(
                form=assessment.assessment_form,
                registry=hashing.hashed,
                title=registry.title,
                location=registry.location,
                type=registry.type,
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
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(initiative__partner_organization=self.request.user.partner)

        return queryset

    def get(self, request, *args, **kwargs):

        headers = {

            'initiative__title': 'Initiative Title',
            'initiative__location': 'Initiative Location',
            'initiative__member__youth__first_name': 'First Name',
            'initiative__member__youth__last_name': 'Last Name',
            'initiative__type': 'Type of Initiative',
            'initiative__duration': 'Duration of the initiative',
            # 'initiative__knowledge_areas': 'Knowledge Areas',
            'initiative__why_this_initiative': 'Why this initiative?',
            'initiative__number_of_beneficiaries': 'Number of beneficiary',
            'initiative__age_of_beneficiaries': 'Age of beneficiaries',
            'initiative__sex_of_beneficiaries': 'Sex of beneficiaries',
            'initiative__indirect_beneficiaries': 'Indirect beneficiaries',
            'initiative__needs_resources': 'Needing resources',
            'initiative__resources_from': 'Resources from?',
            'initiative__resources_type': 'Resources type',
            'initiative__description': 'Description',
            'assertiveness': 'The group feels certain that the initiative will address the problem(s) faced by our communities',
            'mentorship_helpful': 'The group expects to find the mentorship in the planning phase very helpful',
            'problem_addressed': 'Can you tell us more about the problem you/your community is facing?',
            'planned_results': 'Can you please tell us your planned results/what will the initiative achieve? ',


        }

        qs = self.get_queryset().extra(select={

            'assertiveness': "new_data->>'assertiveness'",
            'mentorship_helpful': "new_data->>'mentorship_helpful'",
            'problem_addressed': "new_data->>'problem_addressed'",
            'planned_results': "new_data->>'planned_results'",


        }).values(
            'initiative__title',
            'initiative__member__youth__last_name',
            'initiative__member__youth__first_name',
            'initiative__location',
            'initiative__type',
            'initiative__duration',
            # 'initiative__knowledge_areas',
            'initiative__why_this_initiative',
            'initiative__number_of_beneficiaries',
            'initiative__age_of_beneficiaries',
            'initiative__sex_of_beneficiaries',
            'initiative__indirect_beneficiaries',
            'initiative__needs_resources',
            'initiative__resources_from',
            'initiative__resources_type',
            'initiative__description',
            'assertiveness',
            'mentorship_helpful',
            'problem_addressed',
            'planned_results',



        )

        filename = 'Initiative-Export'

        return render_to_csv_response(qs, filename,  field_header_map=headers)
