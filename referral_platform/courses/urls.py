
from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import CoursesOverview, LifeSkillsPreSkillsAssessmentView, DigitalSkillsAssessmentView

urlpatterns = [

    url(r'^(?P<track>\w+)$', CoursesOverview.as_view(), name='overview'),
    url(r'^(?P<track>\w+)/lifeskills$', LifeSkillsPreSkillsAssessmentView.as_view(), name='lifeskills'),
    url(r'^(?P<track>\w+)/digitalskills$', DigitalSkillsAssessmentView.as_view(), name='digitalskills'),

]
