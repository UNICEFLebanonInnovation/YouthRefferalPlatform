from django.conf.urls import include, url
from django.views.generic import TemplateView
from . import views
from .views import YouthLedentView, AddView, YouthAssessment

urlpatterns = [

    # url(r'^youth-led$', YouthInitiativeView.as_view(), name='youth-led'),
    url(
        regex=r'^add/$',
        view=views.AddView.as_view(),
        name='add-entrepreneurship'
    ),
    url(
        regex=r'^list/$',
        view=views.YouthLedentView.as_view(),
        name='list-entrepreneurship'
    ),
    url(
        regex=r'^edit/(?P<pk>[\w.@+-]+)/$',
        view=views.EditView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^assessment/(?P<pk>[\w.@+-]+)/$',
        view=views.YouthAssessment.as_view(),
        name='assessment'
    ),
    # url(
    #     regex=r'^export-initiative-assessments/$',
    #     view=views.ExportInitiativeAssessmentsView.as_view(),
    #     name='export_ent_assessments'
    # ),
    # url(
    #     regex=r'^exec-sequence/$',
    #     view=views.ExecSequenceView.as_view(),
    #     name='exec_sequence'
    # ),


]
