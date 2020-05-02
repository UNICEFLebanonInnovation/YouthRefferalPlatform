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

    def get_context_data(self, **kwargs):
        powerbi_url = None

        return {
            'powerbi_url': powerbi_url,
        }


class PartnerView(LoginRequiredMixin,
                  GroupRequiredMixin,
                  TemplateView):

    template_name = 'dashboard/partner.html'

    group_required = [u"YOUTH"]

    def handle_no_permission(self):
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        return {
            'powerbi_url': self.request.user.partner.dashboard_url,
        }
