from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from referral_platform.users.views import UserRegisteredMixin

from .forms import LifeSkillsAssessmentForm


class CoursesOverview(UserRegisteredMixin, TemplateView):

    def get_template_names(self):
        return [
            'courses/{}/overview.html'.format(self.kwargs.get('track'))
        ]


class LifeSkillsPreSkillsAssessmentView(UserRegisteredMixin, FormView):

    template_name = 'courses/empowerment/pre-skills-assessment.html'
    form_class = LifeSkillsAssessmentForm

