from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from referral_platform.users.views import UserRegisteredMixin

from .forms import YouthLedInitiativePlanningForm
# -*- coding: utf-8 -*-

import json
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
# from .serializers import RegistrationSerializer, AssessmentSubmissionSerializer
from .models import YouthLedInitiative
# from .filters import YouthFilter, YouthPLFilter, YouthSYFilter
# from .tables import BootstrapTable, CommonTable, CommonTableAlt

#
# class YouthInitiativeView(UserRegisteredMixin, FormView):
#
#     template_name = 'courses/community/initiative.html'
#     form_class = YouthLedInitiativePlanningForm


class AddInitiativeView(LoginRequiredMixin, FormView):

    template_name = 'initiatives/initiatives.html'
    model = YouthLedInitiative
    success_url = '/registrations/list/'
    form_class = YouthLedInitiativePlanningForm

    # def get_success_url(self):
    #     if self.request.POST.get('save', None):
    #         del self.request.session['instance_id']
    #         return '/initiatives/add/'
    #     # if self.request.POST.get('save_and_continue', None):
    #     #     return '/registrations/edit/' + str(self.request.session.get('instance_id')) + '/'
    #     # return self.success_url
    #
    # def get_initial(self):
    #     # force_default_language(self.request, 'ar-ar')
    #     data = dict()
    #     if self.request.user.partner:
    #         data['partner_locations'] = self.request.user.partner.locations.all()
    #         data['partner'] = self.request.user.partner
    #
    #     if self.request.GET.get('youth_id'):
    #             instance = YoungPerson.objects.get(id=self.request.GET.get('youth_id'))
    #             data['youth_id'] = instance.id
    #             data['youth_first_name'] = instance.first_name
    #             data['youth_father_name'] = instance.father_name
    #             data['youth_last_name'] = instance.last_name
    #             data['youth_birthday_day'] = instance.birthday_day
    #             data['youth_birthday_month'] = instance.birthday_month
    #             data['youth_birthday_year'] = instance.birthday_year
    #             data['youth_sex'] = instance.sex
    #             data['youth_nationality'] = instance.nationality_id
    #             data['youth_marital_status'] = instance.marital_status
    #
    #     initial = data
    #     return initial
    #
    # def form_valid(self, form):
    #     form.save(request=self.request)
    #     return super(AddInitiativeView, self).form_valid(form)


# class EditView(LoginRequiredMixin, FormView):
#     template_name = 'registrations/form.html'
#     # form_class = CommonForm
#     model = Registration
#     success_url = '/registrations/list/'
#
#     def get_success_url(self):
#         if self.request.POST.get('save_add_another', None):
#             return '/registrations/add/'
#         return self.success_url
#
#     def get_initial(self):
#         data = dict()
#         if self.request.user.partner:
#             data['partner_locations'] = self.request.user.partner.locations.all()
#             data['partner'] = self.request.user.partner
#         initial = data
#         return initial
#
#     def get_form(self, form_class=None):
#         beneficiary_flag = self.request.user.is_beneficiary
#         if beneficiary_flag:
#             form_class = BeneficiaryCommonForm
#             form = BeneficiaryCommonForm
#         else:
#             form_class = CommonForm
#             form = CommonForm
#
#         instance = Registration.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
#         if self.request.method == "POST":
#             return form(self.request.POST, instance=instance)
#         else:
#             data = RegistrationSerializer(instance).data
#             data['youth_nationality'] = data['youth_nationality_id']
#             data['partner_locations'] = self.request.user.partner.locations.all()
#             data['partner'] = self.request.user.partner
#             return form(data, instance=instance)
#
#     def form_valid(self, form):
#         instance = Registration.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
#         form.save(request=self.request, instance=instance)
#         return super(EditView, self).form_valid(form)
#
