# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import tablib
from django.db.models import Q

from django.views.generic import ListView, FormView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import RedirectView
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework import viewsets, mixins, permissions

from rest_framework.generics import DestroyAPIView
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin

from import_export.formats import base_formats

from referral_platform.users.views import UserRegisteredMixin
from referral_platform.users.utils import force_default_language
from referral_platform.registrations.models import Assessment, AssessmentSubmission
from .models import YoungPerson
from .serializers import YoungPersonSerializer
from .filters import YouthFilter, YouthPLFilter, YouthSYFilter
from .tables import BootstrapTable, CommonTable
from .forms import CommonForm, RegistrationForm


class ListingView(LoginRequiredMixin,
                  FilterView,
                  ExportMixin,
                  SingleTableView,
                  RequestConfig):

    table_class = CommonTable
    model = YoungPerson
    template_name = 'youth/list.html'
    table = BootstrapTable(YoungPerson.objects.all(), order_by='id')

    filterset_class = YouthFilter

    # def get_table_class(self):
    #     locations = [g.p_code for g in self.request.user.partner.locations.all()];
    #     if "PALESTINE" in locations:
    #         return YouthPLFilter
    #     elif "SYRIA" in locations:
    #         return YouthSYFilter
    #     elif "JORDAN" in locations:
    #         return CommonTable

    def get_queryset(self):
        return YoungPerson.objects.filter(partner_organization=self.request.user.partner)

    def get_filterset_class(self):
        locations = [g.p_code for g in self.request.user.partner.locations.all()]
        if "PALESTINE" in locations:
            return YouthPLFilter
        elif "SYRIA" in locations:
            return YouthSYFilter
        elif "JORDAN" in locations:
            return YouthFilter


class AddView(LoginRequiredMixin, CreateView):
    template_name = 'youth/form.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/youth/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def form_valid(self, form):
        instance = form.save(self.request)
        instance.partner_organization = self.request.user.partner
        instance.save()

        return super(AddView, self).form_valid(form)


class DeleteYouthView(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 #viewsets.GenericViewSet,
                 DestroyAPIView):
    """
    Provides API operations around a Enrollment record
    TAREK NOTES: REVERT THIS TO USE API MODULE to USE FULL CRUD OPERATIONS.
    """
    queryset = YoungPerson.objects.all()

    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        return super(DeleteYouthView, self).delete(request, *args, **kwargs)


class YoungPersonViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    model = YoungPerson
    queryset = YoungPerson.objects.all()
    serializer_class = YoungPersonSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #return YoungPerson.objects.filter(partner_organization=self.request.user.partner)
        if self.request.method in ["PATCH", "POST", "PUT"]:
            return self.queryset
        terms = self.request.GET.get('term', 0)
        if terms:
            for term in terms.split():
                qs = self.queryset.filter(
                    Q(first_name__contains=term) |
                    Q(father_name__contains=term) |
                    Q(last_name__contains=term) |
                    Q(id_number__contains=term)
                ).distinct()
            return qs

    def delete(self, request, *args, **kwargs):
        instance = self.model.objects.get(id=kwargs['pk'])
        instance.delete()
        return JsonResponse({'status': status.HTTP_200_OK})


class EditView(LoginRequiredMixin, UpdateView):
    template_name = 'youth/form.html'
    form_class = CommonForm
    model = YoungPerson
    success_url = '/youth/'

    def get_success_url(self):
        if self.request.POST.get('save_add_another', None):
            return '/youth/add/'
        return self.success_url

    def get_initial(self):
        data = dict()
        if self.request.user.partner:
            data['partner_locations'] = self.request.user.partner.locations.all()
            data['partner'] = self.request.user.partner
        initial = data
        return initial

    def form_valid(self, form):
        form.save(self.request)
        return super(EditView, self).form_valid(form)
