from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView
from django.db.models import Count, Min, Sum, Avg

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PartnerOrganization
from referral_platform.courses.models import Enrollment
from referral_platform.youth.models import Nationality


class PartnerView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/home.html'

    def _build_age_sex_matrix(self, queryset, percentage=True):

        matrix = {}
        nationalities = Nationality.objects.all()
        for sex in ['Female', 'Male']:
            matrix['{}_total'.format(sex)] = queryset.filter(youth__sex=sex).count()
            for nationality in nationalities:
                total = queryset.filter(youth__sex=sex, youth__nationality__code=nationality.code).count()
                matrix['{}_{}'.format(sex, nationality.code)] = float(total) / float(queryset.count()) * 100 \
                    if percentage and total else total
        return matrix

    def get_context_data(self, **kwargs):
        location = int(self.request.GET.get('location', 0))

        enrollments = Enrollment.objects.all()
        if location:
            enrollments = enrollments.filter(location=location)

        locations = []
        if self.request.user.partner:
            locations = self.request.user.partner.locations.all()

        # digitalskills
        digitalskills_enrollments = enrollments.filter(course__slug='digitalskills')
        digitalskills_enrolled = {
            'total': digitalskills_enrollments.count(),
        }
        digitalskills_enrolled.update(self._build_age_sex_matrix(digitalskills_enrollments, percentage=False))

        # healthy indicator
        digitalskills_complete = digitalskills_enrollments.filter(status='post_test')
        digitalskills_improved = {
            'total': float(digitalskills_complete.count()) / float(digitalskills_enrollments.count()) * 100 if digitalskills_complete.count() else 0
        }
        digitalskills_improved.update(self._build_age_sex_matrix(digitalskills_complete, percentage=True))


        # lifeskills
        lifeskills_enrollments = enrollments.filter(course__slug='lifeskills')
        lifeskills_enrolled = {
            'total': lifeskills_enrollments.count(),
        }
        lifeskills_enrolled.update(self._build_age_sex_matrix(lifeskills_enrollments, percentage=False))

        lifeskills_complete = lifeskills_enrollments.filter(status='post_test')

        # healthy indicator
        lifeskills_improved = lifeskills_complete.filter(scores__healthy_improved=True)
        lifeskills_healthy_lifestyles = {
            'total': float(lifeskills_improved.count()) / float(lifeskills_enrollments.count()) * 100 if lifeskills_improved.count() else 0
        }
        lifeskills_healthy_lifestyles.update(self._build_age_sex_matrix(lifeskills_improved))

        # empowerment indicator
        lifeskills_empowered = lifeskills_complete.filter(scores__empowered_improved=True)
        lifeskills_feeling_empowered = {
            'total': float(lifeskills_empowered.count()) * float(lifeskills_enrollments.count()) * 100 if lifeskills_empowered.count() else 0
        }
        lifeskills_feeling_empowered.update(self._build_age_sex_matrix(lifeskills_empowered))

        return {
            'location': location,
            'locations': locations,
            'digitalskills_enrolled': digitalskills_enrolled,
            'digitalskills_improved': digitalskills_improved,
            'lifeskills_enrolled': lifeskills_enrolled,
            'lifeskills_healthy_lifestyles': lifeskills_healthy_lifestyles,
            'lifeskills_feeling_empowered': lifeskills_feeling_empowered
        }


class PartnerHomeView(LoginRequiredMixin, TemplateView):

    template_name = 'partner/profile.html'
