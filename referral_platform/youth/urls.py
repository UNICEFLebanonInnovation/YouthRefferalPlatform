
from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import HomeView, RegistrationView
from . import views

urlpatterns = [

    # url(r'^$', HomeView.as_view(), name='home'),
    # url(r'^registration$', RegistrationView.as_view(), name='registration'),

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
        regex=r'^$',
        view=views.ListingView.as_view(),
        name='list'
    ),
    url(
        regex=r'^export/$',
        view=views.ExportView.as_view(),
        name='export'
    ),
]


