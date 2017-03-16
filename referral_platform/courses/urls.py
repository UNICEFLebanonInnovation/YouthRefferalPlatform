
from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import CoursesOverview, LifeSkillsPreSkillsAssessmentView

urlpatterns = [

    url(r'^(?P<track>\w+)$', CoursesOverview.as_view(), name='overview'),
    url(r'^(?P<track>\w+)/preskills$', LifeSkillsPreSkillsAssessmentView.as_view(), name='preskills'),

]
