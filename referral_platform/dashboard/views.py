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

        country = self.request.user.country_id
        print (country)
        if country ==50:
            powerbi_url = ''
        elif country ==1:
            powerbi_url='https://app.powerbi.com/view?r=eyJrIjoiMjg1NzRjY2UtM2U3MS00NjU2LTlmMmYtMzRhY2E3M2QzMmZkIiwidCI6Ijc3NDEwMTk1LTE0ZTEtNGZiOC05MDRiLWFiMTg5MjAyMzY2NyIsImMiOjh9&pageName=ReportSection9ad8159084a3dd930461'
        elif country ==2:
            powerbi_url = 'https://app.powerbi.com/view?r=eyJrIjoiM2FiYjk2NWUtMjQ2NS00Y2M2LTkzOWEtYWU1NWM5ZGRmNmQ3IiwidCI6Ijc3NDEwMTk1LTE0ZTEtNGZiOC05MDRiLWFiMTg5MjAyMzY2NyIsImMiOjh9'
        elif country ==3:
            powerbi_url = 'https://app.powerbi.com/view?r=eyJrIjoiZGJkNDZiOGQtOTM4NS00YTMwLWIwMjQtZjgyZDMxMGQyZDM3IiwidCI6Ijc3NDEwMTk1LTE0ZTEtNGZiOC05MDRiLWFiMTg5MjAyMzY2NyIsImMiOjh9'
        else:
            powerbi_url=''

        print('url is:' + powerbi_url)
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

        country = self.request.user.country_id
        print (country)

        if country ==50:
            powerbi_url = ''
        elif country ==1:
            powerbi_url = 'https://app.powerbi.com/view?r=eyJrIjoiMjg1NzRjY2UtM2U3MS00NjU2LTlmMmYtMzRhY2E3M2QzMmZkIiwidCI6Ijc3NDEwMTk1LTE0ZTEtNGZiOC05MDRiLWFiMTg5MjAyMzY2NyIsImMiOjh9&pageName=ReportSection9ad8159084a3dd930461'
        elif country ==2:
            powerbi_url = 'https://app.powerbi.com/view?r=eyJrIjoiM2FiYjk2NWUtMjQ2NS00Y2M2LTkzOWEtYWU1NWM5ZGRmNmQ3IiwidCI6Ijc3NDEwMTk1LTE0ZTEtNGZiOC05MDRiLWFiMTg5MjAyMzY2NyIsImMiOjh9'
        elif country ==3:
            powerbi_url = 'https://app.powerbi.com/view?r=eyJrIjoiZGJkNDZiOGQtOTM4NS00YTMwLWIwMjQtZjgyZDMxMGQyZDM3IiwidCI6Ijc3NDEwMTk1LTE0ZTEtNGZiOC05MDRiLWFiMTg5MjAyMzY2NyIsImMiOjh9'

        else:
            powerbi_url = ''

        print('url is:' + powerbi_url)
        return {
            'powerbi_url': powerbi_url}

