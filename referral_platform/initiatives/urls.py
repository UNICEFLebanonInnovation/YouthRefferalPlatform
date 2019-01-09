from django.conf.urls import include, url
from django.views.generic import TemplateView
from . import views
from .views import YouthInitiativeView

urlpatterns = [

    # url(r'^youth-led$', YouthInitiativeView.as_view(), name='youth-led'),
    url(
        regex=r'^add/$',
        view=views.AddView.as_view(),
        name='add-initiative'
    ),
    url(
        regex=r'^list/$',
        view=views.YouthInitiativeView.as_view(),
        name='list-initiatives'
    ),
    url(
        regex=r'^edit/(?P<pk>[\w.@+-]+)/$',
        view=views.EditView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^assessment/(?P<slug>[\w.@+-]+)/$',
        view=views.YouthAssessment.as_view(),
        name='assessment'
    ),
    url(
        regex=r'^export-initiative-assessments/$',
        view=views.ExportInitiativeAssessmentsView.as_view(),
        name='export_initiative_assessments'
    ),
    # url(
    #     regex=r'^assessment/submission/$',
    #     view=views.YouthAssessmentSubmission.as_view(),
    #     name='submission'
    # ),
    # (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

]
