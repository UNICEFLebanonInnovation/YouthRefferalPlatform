# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from rest_framework import status
from rest_framework import viewsets, mixins, permissions
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableView
from django_tables2.export.views import ExportMixin

from .models import Exporter
from .filters import ExporterFilter
from .tables import BootstrapTable, ExporterTable
from .exporter import export_full_data
from .serializers import ExporterSerializer
from referral_platform.partners.models import PartnerOrganization
from referral_platform.users.utils import has_group


class ExporterView(LoginRequiredMixin,
                   GroupRequiredMixin,
                   TemplateView):

    template_name = 'backends/exporter.html'

    group_required = [u"EXPORT_FULL"]

    def handle_no_permission(self, request):
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        if self.request.GET.get('report', None):
            #  todo raise a exception if the partner do not belongs to the CO
            data = {
                'report': self.request.GET.get('report'),
                'user': self.request.user.id,
                'partner': self.request.GET.get('partner', None),
            }
            export_full_data(data)
        partners = PartnerOrganization.objects.all()

        if has_group(self.request.user, 'UNICEF_CO'):
            partners = partners.filter(locations=self.request.user.country.id)
        return {
            'partners': partners,
        }


class ExporterViewSet(LoginRequiredMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,):

    model = Exporter
    queryset = Exporter.objects.all()
    serializer_class = ExporterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def handle_no_permission(self, request):
        return HttpResponseForbidden()

    def list(self, request, *args, **kwargs):
        if self.request.GET.get('report', None):
            #  todo raise a exception if the partner do not belongs to the CO
            data = {
                'report': self.request.GET.get('report'),
                'user': self.request.user.id,
                'partner': self.request.user.partner_id
            }
            export_full_data(data)
        return JsonResponse({'status': status.HTTP_200_OK})


class ExporterListView(LoginRequiredMixin,
                       FilterView,
                       ExportMixin,
                       SingleTableView,
                       RequestConfig):

    table_class = ExporterTable
    model = Exporter
    template_name = 'backends/files.html'
    table = BootstrapTable(Exporter.objects.all(), order_by='-id')

    filterset_class = ExporterFilter

    def get_queryset(self):
        if has_group(self.request.user, 'UNICEF_CO'):
            return Exporter.objects.filter(exported_by=self.request.user)
        if has_group(self.request.user, 'YOUTH'):
            return Exporter.objects.filter(partner=self.request.user.partner)

        return Exporter.objects.filter(exported_by=self.request.user)
