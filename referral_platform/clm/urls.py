from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^add/$',
        view=views.YouthAddView.as_view(),
        name='add'
    ),
    url(
        regex=r'^edit/(?P<pk>[\w.@+-]+)/$',
        view=views.YouthEditView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^assessment/list/(?P<slug>[\w.@+-]+)/$',
        view=views.YouthAssessment.as_view(),
        name='assessment'
    ),
    url(
        regex=r'^assessment/submission/$',
        view=views.YouthAssessmentSubmission.as_view(),
        name='submission'
    ),
    url(
        regex=r'^$',
        view=views.YouthListView.as_view(),
        name='list'
    ),
]
