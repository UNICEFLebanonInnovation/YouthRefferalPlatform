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
        view=views.BLNAddView.as_view(),
        name='bln_add'
    ),
    url(
        regex=r'^bln-edit/(?P<pk>[\w.@+-]+)/$',
        view=views.BLNEditView.as_view(),
        name='bln_edit'
    ),
    url(
        regex=r'^bln-assessment/(?P<pk>[\w.@+-]+)/$',
        view=views.BLNAssessmentSubmission.as_view(),
        name='bln_assessment'
    ),
    url(
        regex=r'^bln-list/$',
        view=views.BLNListView.as_view(),
        name='bln_list'
    ),

    url(
        regex=r'^rs-add/$',
        view=views.RSAddView.as_view(),
        name='rs_add'
    ),
    url(
        regex=r'^rs-edit/(?P<pk>[\w.@+-]+)/$',
        view=views.RSEditView.as_view(),
        name='rs_edit'
    ),
    url(
        regex=r'^rs-list/$',
        view=views.RSListView.as_view(),
        name='rs_list'
    ),

    url(
        regex=r'^cbece-add/$',
        view=views.CBECEAddView.as_view(),
        name='cbece_add'
    ),
    url(
        regex=r'^cbece-edit/(?P<pk>[\w.@+-]+)/$',
        view=views.CBECEEditView.as_view(),
        name='cbece_edit'
    ),
    url(
        regex=r'^cbece-list/$',
        view=views.CBECEListView.as_view(),
        name='cbece_list'
    ),
]
