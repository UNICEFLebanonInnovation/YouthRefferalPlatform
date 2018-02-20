
from django.conf.urls import include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = [

    url(
        regex=r'^add/$',
        view=views.AddView.as_view(),
        name='add'
    ),
    url(
        regex=r'^edit/(?P<pk>[\w.@+-]+)/$',
        view=views.EditView.as_view(),
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
        regex=r'^list/$',
        view=views.ListingView.as_view(),
        name='list'
    ),
    url(
        regex=r'^export/$',
        view=views.ExportView.as_view(),
        name='export'
    ),

    url(
        regex=r'^export-registry-assessments/$',
        view=views.ExportRegistryAssessmentsView.as_view(),
        name='export_registry_assessments'
    ),

    url(
        regex=r'^export-pre-assessments/$',
        view=views.ExportPreAssessmentView.as_view(),
        name='export_pre_assessments'
    ),

    url(
        regex=r'^export-post-assessments/$',
        view=views.ExportPostAssessmentView.as_view(),
        name='export_post_assessments'
    ),

    url(
        regex=r'^export-pre-entrepreneurship/$',
        view=views.ExportPreEntrepreneurshipView.as_view(),
        name='export_pre_entrepreneurship'
    ),

    url(
        regex=r'^export-post-entrepreneurship/$',
        view=views.ExportPostEntrepreneurshipView.as_view(),
        name='export_post_entrepreneurship'
    ),
]


