from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PartnerOrganization
from referral_platform.courses.models import Enrollment


class PartnerView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/home.html'

    def get_context_data(self, **kwargs):
        location = int(self.request.GET.get('location', 0))

        enrollments = Enrollment.objects.filter(location_id=location)

        locations = []
        if self.request.user.partner:
            locations = self.request.user.partner.locations.all()

        return {
            'location': location,
            'locations': locations
        }


class PartnerHomeView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/profile.html'
