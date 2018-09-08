from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^CO/$',
        view=views.COView.as_view(),
        name='co'
    ),
    # url(
    #     regex=r'^partner/$',
    #     view=views.PartnerView.as_view(),
    #     name='partner'
    # ),
]
