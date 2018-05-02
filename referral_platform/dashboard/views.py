# from django.http import HttpResponse
# from django.template import loader
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin


class COView(LoginRequiredMixin,
             # GroupRequiredMixin,
             TemplateView):

    template_name = 'dashboard/co.html'

    # group_required = [u"UNICEF_CO"]

    def handle_no_permission(self, request):
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        powerbi_url = None
        if self.request.user.country_id == 3 or \
            (self.request.user.partner and self.request.user.partner.has_country(3)):
            powerbi_url = settings.POWERBI_JCO
        if self.request.user.country_id == 2 or \
            (self.request.user.partner and self.request.user.partner.has_country(2)):
            powerbi_url = settings.POWERBI_SCO
        if self.request.user.country_id == 1 or \
            (self.request.user.partner and self.request.user.partner.has_country(1)):
            powerbi_url = settings.POWERBI_PCO

        return {
            'powerbi_url': powerbi_url,
        }


class PartnerView(LoginRequiredMixin,
                   GroupRequiredMixin,
                   TemplateView):

    template_name = 'dashboard/partner.html'

    group_required = [u"YOUTH"]

    def handle_no_permission(self, request):
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        return {
            'powerbi_url': self.request.user.partner.dashboard_url,
        }
