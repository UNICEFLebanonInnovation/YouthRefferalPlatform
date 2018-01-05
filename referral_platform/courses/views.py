from __future__ import absolute_import, unicode_literals

import json
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView, DetailView, RedirectView, View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator

from referral_platform.users.views import UserRegisteredMixin
from referral_platform.youth.models import YoungPerson
from referral_platform.locations.models import Location

from .models import Enrollment, Course, Path


class CoursesOverview(UserRegisteredMixin, DetailView):

    model = Path
    slug_url_kwarg = 'path'
    context_object_name = 'path'
    template_name = 'courses/overview.html'

    def get_context_data(self, **kwargs):
        locations = self.request.user.profile.partner_organization.locations
        enrollement = Enrollment.objects.filter(
            youth=self.request.user.profile,
            course__path=self.object
        ).last()
        kwargs.update({'enrollment': enrollement, 'locations': locations})
        return super(CoursesOverview, self).get_context_data(**kwargs)


class CourseAssessment(UserRegisteredMixin, SingleObjectMixin, RedirectView):

    model = Course
    slug_url_kwarg = 'course'

    def get_redirect_url(self, *args, **kwargs):
        course = self.get_object()
        youth = self.request.user.profile
        location = Location.objects.get(id=self.request.GET.get('location'))
        enrollment, new = Enrollment.objects.get_or_create(youth=youth, course=course, location=location)

        url = '{form}?d[youth_id]={id}&d[status]={status}&returnURL={callback}'.format(
            form = course.assessment_form,
            id = youth.number,
            status = Enrollment.STATUS.pre_test if enrollment.status == Enrollment.STATUS.enrolled
            else Enrollment.STATUS.post_test,
            callback = self.request.build_absolute_uri(
                reverse('courses:overview', kwargs={'path': course.path.slug})
            )
        )
        return url


@method_decorator(csrf_exempt, name='dispatch')
class CourseAssessmentSubmission(SingleObjectMixin, View):

    model = Course
    slug_url_kwarg = 'course'

    def post(self, request, *args, **kwargs):
        if 'youth_id' not in request.body or 'status' not in request.body:
            return HttpResponseBadRequest()

        payload = json.loads(request.body.decode('utf-8'))

        enrollment = get_object_or_404(
            Enrollment,
            course=self.get_object(),
            youth__number=payload['youth_id']
        )

        enrollment.status = payload['status']
        setattr(enrollment, payload['status'], payload)

        if enrollment.course.slug == 'lifeskills':
            keys = [
                'lifestyle/use_soap',
                'lifestyle/wash_hands_after_toilet',
                'lifestyle/take_baths',
                'lifestyle/brush_teeth'
                'lifestyle/eat_well',
                'lifestyle/exercise',
                'lifestyle/limit_screen_time',
                'lifestyle/respect_environment',
            ]
            enrollment.score('healthy', enrollment.status, keys)

            keys = [
                'comm_skills/articulation',
                'comm_skills/express_opinions',
                'self_esteem/satisfied',
                'self_esteem/good_qualities',
                'self_esteem/set_goals',
                'self_esteem/make_decisions',
                'self_esteem/solve_problems',
                'analysis/clarify_issues',
                'analysis/take_advice',
                'analysis/no_wrong_activities',
                'analysis/determine_facts',
                'analysis/consider_options',
                'analysis/creative_ideas',
                'team_building/build_on_ideas',
                'team_building/constructive_feedback',
                'social_cohesion/trust_peers'

            ]
            enrollment.score('empowered', enrollment.status, keys)

        enrollment.save()

        return HttpResponse()



