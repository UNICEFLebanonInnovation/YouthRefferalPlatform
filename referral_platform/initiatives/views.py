from __future__ import absolute_import, unicode_literals
from .tables import BootstrapTable, CommonTable, CommonTableAlt
from django.views.generic import TemplateView, FormView
from django.views.generic import ListView, FormView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext as _
from django.db.models import Q

from rest_framework import status
from rest_framework import viewsets, mixins, permissions
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin
from import_export.formats import base_formats
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin
from django.contrib.auth.mixins import LoginRequiredMixin


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
    success_url = 'initiatives/list.html'
    form_class = YouthLedInitiativePlanningForm
    form = YouthLedInitiativePlanningForm

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/initiatives/add/'
        return self.success_url

    def get_initial(self):
        # force_default_language(self.request, 'ar-ar')
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner_organization'] = self.request.user.partner
            data['members'] = YoungPerson.objects.filter(partner_organization=self.request.user.partner, )

        # if self.request.GET.get('youth_id'):
        #         instance = YoungPerson.objects.get(id=self.request.GET.get('youth_id'))
        #         data['youth_id'] = instance.id
        #         data['youth_first_name'] = instance.first_name
        #         data['youth_father_name'] = instance.father_name
        #         data['youth_last_name'] = instance.last_name
        #         data['youth_birthday_day'] = instance.birthday_day
        #         data['youth_birthday_month'] = instance.birthday_month
        #         data['youth_birthday_year'] = instance.birthday_year
        #         data['youth_sex'] = instance.sex
        #         data['youth_nationality'] = instance.nationality_id
        #         data['youth_marital_status'] = instance.marital_status

        initial = data
        return initial

    def get_form(self, form_class=None):
        form_class = YouthLedInitiativePlanningForm
        # instance = YouthLedInitiative.objects.get(partner_organization=self.request.user.partner)
        if self.request.method == "POST":
            return form_class(self.request.POST)
        else:
            return form_class()

    def form_valid(self, form):
        # instance = YouthLedInitiative.objects.get(id=self.kwargs['pk'], partner_organization=self.request.user.partner)
        form.save(request=self.request)
        return super(AddView, self).form_valid(form)




