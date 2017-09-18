
from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import CoursesOverview, CourseAssessment, CourseAssessmentSubmission

urlpatterns = [

    url(r'^(?P<path>[-\w]+)$', CoursesOverview.as_view(), name='overview'),
    url(r'^(?P<path>[-\w]+)/(?P<course>[-\w]+)$', CourseAssessment.as_view(), name='assessment'),
    url(r'^(?P<path>[-\w]+)/(?P<course>[-\w]+)/submit$', CourseAssessmentSubmission.as_view())
]
