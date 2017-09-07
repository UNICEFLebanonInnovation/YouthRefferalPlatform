# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.views.generic import ListView, FormView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.db.models import Q

import tablib
from rest_framework import status
from rest_framework import viewsets, mixins, permissions
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin
from import_export.formats import base_formats

from referral_platform.users.templatetags.util_tags import has_group

from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin

from .filters import BLNFilter, RSFilter, CBECEFilter
from .tables import BootstrapTable, BLNTable, RSTable, CBECETable

from referral_platform.outreach.models import Child
from referral_platform.outreach.serializers import ChildSerializer
from .models import BLN, RS, CBECE
from .forms import BLNForm, RSForm, CBECEForm
from .serializers import BLNSerializer, RSSerializer, CBECESerializer


class CLMView(LoginRequiredMixin,
            # GroupRequiredMixin,
            TemplateView):

    template_name = 'clm/index.html'

    # group_required = [u"ENROL_EDIT"]

    def get_context_data(self, **kwargs):
        return {}


class BLNAddView(LoginRequiredMixin,
                     # GroupRequiredMixin,
                     FormView):

    template_name = 'clm/bln_add.html'
    form_class = BLNForm
    success_url = '/clm/bln-list/'

    def get_context_data(self, **kwargs):
        # force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(BLNAddView, self).get_context_data(**kwargs)

    def get_initial(self):
        initial = super(BLNAddView, self).get_initial()
        data = []
        if self.request.GET.get('enrollment_id'):
            instance = BLN.objects.get(id=self.request.GET.get('enrollment_id'))
            data = BLNSerializer(instance).data
        if self.request.GET.get('student_outreach_child'):
            instance = Child.objects.get(id=int(self.request.GET.get('student_outreach_child')))
            data = ChildSerializer(instance).data
        initial = data

        return initial

    def form_valid(self, form):
        form.save(self.request)
        return super(BLNAddView, self).form_valid(form)


class BLNEditView(LoginRequiredMixin,
                         # GroupRequiredMixin,
                         FormView):

    template_name = 'clm/bln_edit.html'
    form_class = BLNForm
    success_url = '/clm/bln-list/'

    def get_context_data(self, **kwargs):
        # force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(BLNEditView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        instance = BLN.objects.get(id=self.kwargs['pk'])
        if self.request.method == "POST":
            return BLNForm(self.request.POST, instance=instance, request=self.request)
        else:
            data = BLNSerializer(instance).data
            data['student_nationality'] = data['student_nationality_id']
            return BLNForm(data, instance=instance, request=self.request)

    def form_valid(self, form):
        instance = BLN.objects.get(id=self.kwargs['pk'])
        form.save(request=self.request, instance=instance)
        return super(BLNEditView, self).form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class BLNAssessmentSubmission(SingleObjectMixin, View):

    model = BLN
    slug_url_kwarg = 'status'

    def post(self, request, *args, **kwargs):

        if 'status' not in request.body:
            return HttpResponseBadRequest()

        payload = json.loads(request.body.decode('utf-8'))

        enrollment = BLN.objects.get(id=self.kwargs['pk'])

        enrollment.status = payload['status']
        setattr(enrollment, payload['status'], payload)

        return HttpResponse()


class BLNListView(LoginRequiredMixin,
                  FilterView,
                  ExportMixin,
                  SingleTableView,
                  RequestConfig):

    table_class = BLNTable
    model = BLN
    template_name = 'clm/bln_list.html'
    table = BootstrapTable(BLN.objects.all(), order_by='id')

    filterset_class = BLNFilter

    def get_queryset(self):
        return BLN.objects.filter(owner=self.request.user)


class RSAddView(LoginRequiredMixin,
                # GroupRequiredMixin,
                FormView):

    template_name = 'clm/rs_add.html'
    form_class = RSForm
    success_url = '/clm/rs-list/'

    def get_context_data(self, **kwargs):
        # force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(RSAddView, self).get_context_data(**kwargs)

    def get_initial(self):
        initial = super(RSAddView, self).get_initial()
        data = []
        if self.request.GET.get('enrollment_id'):
            instance = RS.objects.get(id=self.request.GET.get('enrollment_id'))
            data = RSSerializer(instance).data
        if self.request.GET.get('student_outreach_child'):
            instance = Child.objects.get(id=int(self.request.GET.get('student_outreach_child')))
            data = ChildSerializer(instance).data
        initial = data

        return initial

    def form_valid(self, form):
        form.save(self.request)
        return super(RSAddView, self).form_valid(form)


class RSEditView(LoginRequiredMixin,
                 # GroupRequiredMixin,
                 FormView):

    template_name = 'clm/rs_edit.html'
    form_class = RSForm
    success_url = '/clm/rs-list/'

    def get_context_data(self, **kwargs):
        # force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(RSEditView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        instance = RS.objects.get(id=self.kwargs['pk'])
        if self.request.method == "POST":
            RSForm(self.request.POST, instance=instance)
        else:
            data = RSSerializer(instance).data
            return RSForm(data, instance=instance)

    def form_valid(self, form):
        instance = RS.objects.get(id=self.kwargs['pk'])
        form.save(request=self.request, instance=instance)
        return super(RSEditView, self).form_valid(form)


class RSListView(LoginRequiredMixin,
                 FilterView,
                 ExportMixin,
                 SingleTableView,
                 RequestConfig):

    table_class = RSTable
    model = RS
    template_name = 'clm/rs_list.html'
    table = BootstrapTable(RS.objects.all(), order_by='id')

    filterset_class = RSFilter

    def get_queryset(self):
        return RS.objects.filter(owner=self.request.user)


class CBECEAddView(LoginRequiredMixin,
                   # GroupRequiredMixin,
                   FormView):

    template_name = 'clm/cbece_add.html'
    form_class = CBECEForm
    success_url = '/clm/cbece-list/'

    def get_context_data(self, **kwargs):
        # force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(CBECEAddView, self).get_context_data(**kwargs)

    def get_initial(self):
        initial = super(CBECEAddView, self).get_initial()
        data = []
        if self.request.GET.get('enrollment_id'):
            instance = CBECE.objects.get(id=self.request.GET.get('enrollment_id'))
            data = CBECESerializer(instance).data
        if self.request.GET.get('student_outreach_child'):
            instance = Child.objects.get(id=int(self.request.GET.get('student_outreach_child')))
            data = ChildSerializer(instance).data
        initial = data

        return initial

    def form_valid(self, form):
        form.save(self.request)
        return super(CBECEAddView, self).form_valid(form)


class CBECEEditView(LoginRequiredMixin,
                    # GroupRequiredMixin,
                    FormView):

    template_name = 'clm/cbece_edit.html'
    form_class = CBECEForm
    success_url = '/clm/cbece-list/'

    def get_context_data(self, **kwargs):
        # force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(CBECEEditView, self).get_context_data(**kwargs)

    def get_form(self, form_class=None):
        instance = CBECE.objects.get(id=self.kwargs['pk'])
        if self.request.method == "POST":
            CBECEForm(self.request.POST, instance=instance)
        else:
            data = CBECESerializer(instance).data
            return CBECEForm(data, instance=instance)

    def form_valid(self, form):
        instance = CBECE.objects.get(id=self.kwargs['pk'])
        form.save(request=self.request, instance=instance)
        return super(CBECEEditView, self).form_valid(form)


class CBECEListView(LoginRequiredMixin,
                    FilterView,
                    ExportMixin,
                    SingleTableView,
                    RequestConfig):

    table_class = CBECETable
    model = CBECE
    template_name = 'clm/cbece_list.html'
    table = BootstrapTable(CBECE.objects.all(), order_by='id')

    filtecbeceet_class = CBECEFilter

    def get_queryset(self):
        return CBECE.objects.filter(owner=self.request.user)


####################### API VIEWS #############################
