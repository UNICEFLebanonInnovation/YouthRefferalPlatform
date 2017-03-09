from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PartnerOrganization


class PartnerView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/home.html'


class PartnerHomeView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/profile.html'
