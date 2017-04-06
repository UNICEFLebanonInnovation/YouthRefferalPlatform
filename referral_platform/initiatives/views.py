from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from referral_platform.users.views import UserRegisteredMixin

from .forms import YouthLedInitiativePlanningForm


class YouthInitiativeView(UserRegisteredMixin, FormView):

    template_name = 'courses/community/initiative.html'
    form_class = YouthLedInitiativePlanningForm

