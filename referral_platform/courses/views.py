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

from .models import Enrollment, Course, Path
from .forms import LifeSkillsAssessmentForm, DigitalSkillsAssessmentForm


class CoursesOverview(UserRegisteredMixin, DetailView):

    model = Path
    slug_url_kwarg = 'path'
    context_object_name = 'path'
    template_name = 'courses/overview.html'

    def get_context_data(self, **kwargs):

        enrollement = Enrollment.objects.filter(
            youth=self.request.user.profile,
            course__path=self.object
        ).last()
        kwargs.update({'enrollment': enrollement})
        return super(CoursesOverview, self).get_context_data(**kwargs)



class CourseAssessment(UserRegisteredMixin, SingleObjectMixin, RedirectView):

    model = Course
    slug_url_kwarg = 'course'

    def get_redirect_url(self, *args, **kwargs):
        course = self.get_object()
        youth = self.request.user.profile
        new, enrollment = Enrollment.objects.get_or_create(youth=youth, course=course)

        url = '{form}?d[youth_id]={id}&d[status]={status}&returnURL={callback}'.format(
            form = course.assessment_form,
            id = youth.number,
            status = Enrollment.STATUS.pre_test if enrollment.status.enrolled else Enrollment.STATUS.post_test,
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

        enrollment.save()

        return HttpResponse()



