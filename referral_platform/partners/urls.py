from django.conf.urls import include, url

from . import views


urlpatterns = [

    url(r'^$', views.PartnerView.as_view(), name='home'),
    url(r'^profile$', views.PartnerView.as_view(), name='profile'),

]
