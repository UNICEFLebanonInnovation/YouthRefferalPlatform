from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PartnerOrganization


class PartnerView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/home.html'

    def get_context_data(self, **kwargs):
        location = self.request.GET.get('location', 0)
        locations = self.request.user.locations.all()

        return {
            'location': location,
            'locations': locations
        }


class PartnerHomeView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/profile.html'
