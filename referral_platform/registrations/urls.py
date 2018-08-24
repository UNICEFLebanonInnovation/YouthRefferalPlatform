
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
        regex=r'^export-civic-assessments/$',
        view=views.ExportCivicAssessmentsView.as_view(),
        name='export_civic_assessments'
    ),

    url(
        regex=r'^export-entrepreneurship-assessments/$',
        view=views.ExportEntrepreneurshipAssessmentsView.as_view(),
        name='export_entrepreneurship_assessments'
    ),

    url(
        regex=r'^export-initiative-assessments/$',
        view=views.ExportInitiativeAssessmentsView.as_view(),
        name='export_initiative_assessments'
    ),
    url(
        regex=r'^exportPBI/$',
        view=views.exportPBI(),
        name='ZIP'
    ),
]


