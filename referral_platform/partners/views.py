from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.db.models import Count, Min, Sum, Avg

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PartnerOrganization
from referral_platform.courses.models import Enrollment
from referral_platform.youth.models import Nationality


class PartnerView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/home.html'

    def _build_age_sex_matrix(self, queryset):

        matrix = {}
        nationalities = Nationality.objects.all()
        for sex in ['Female', 'Male']:
            matrix['{}_total'.format(sex)] = queryset.filter(youth__sex=sex).count()
            for nationality in nationalities:
                total = queryset.filter(youth__sex=sex, youth__nationality__code=nationality.code).count()
                matrix['{}_{}'.format(sex, nationality.code)] = float(total) / float(queryset.count()) * 100 if total else 0
        return matrix

    def get_context_data(self, **kwargs):
        location = int(self.request.GET.get('location', 0))

        enrollments = Enrollment.objects.all()

        locations = []
        if self.request.user.partner:
            locations = self.request.user.partner.locations.all()

        # lifeskills
        lifeskills_enrollments = enrollments.filter(course__slug='lifeskills')
        lifeskills_complete = lifeskills_enrollments.filter(status='post_test')

        # healthy indicator
        lifeskills_improved = lifeskills_complete.filter(scores__healthy_improved=True)
        lifeskills_healthy_lifestyles = {
            'total_enrolled': lifeskills_enrollments.count(),
            'total_improved': float(lifeskills_improved.count()) / float(lifeskills_enrollments.count()) * 100
        }
        lifeskills_healthy_lifestyles.update(self._build_age_sex_matrix(lifeskills_improved))

        # empowerment indicator
        lifeskills_empowered = lifeskills_complete.filter(scores__empowered_improved=True)
        lifeskills_feeling_empowered = {
            'total_enrolled': lifeskills_enrollments.count(),
            'total_empowered': float(lifeskills_empowered.count()) * float(lifeskills_enrollments.count()) * 100
        }
        lifeskills_feeling_empowered.update(self._build_age_sex_matrix(lifeskills_empowered))

        return {
            'location': location,
            'locations': locations,
            'lifeskills_healthy_lifestyles': lifeskills_healthy_lifestyles,
            'lifeskills_feeling_empowered': lifeskills_feeling_empowered
        }


class PartnerHomeView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/profile.html'
