from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [

    url(
        regex=r'^index/$',
        view=views.CLMView.as_view(),
        name='index'
    ),

    url(
        regex=r'^bln-add/$',
        view=views.YouthAddView.as_view(),
        name='bln_add'
    ),
    url(
        regex=r'^bln-edit/(?P<pk>[\w.@+-]+)/$',
        view=views.YouthEditView.as_view(),
        name='bln_edit'
    ),
    url(
        regex=r'^bln-assessment/(?P<pk>[\w.@+-]+)/$',
        view=views.YouthAssessmentSubmission.as_view(),
        name='bln_assessment'
    ),
    url(
        regex=r'^bln-list/$',
        view=views.YouthListView.as_view(),
        name='bln_list'
    ),

]
