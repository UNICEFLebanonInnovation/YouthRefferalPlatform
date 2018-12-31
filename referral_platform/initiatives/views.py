from __future__ import absolute_import, unicode_literals

import json
import datetime
import time
from .tables import BootstrapTable, CommonTable, CommonTableAlt
from django.views.generic import ListView, FormView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
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

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from referral_platform.registrations.models import Registration, Assessment, AssessmentSubmission, AssessmentHash


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

        url = '{form}?d[registry]={registry}&d[country]={country}&d[partner]={partner}' \
              '&returnURL={callback}'.format(
                form=assessment.assessment_form,
                registry=hashing.hashed,
                partner=registry.partner_organization.name,
                country=registry.governorate.parent.name,
                # nationality=youth.nationality.code,
                callback=self.request.META.get('HTTP_REFERER', registry.get_absolute_url())
        )
        return url
