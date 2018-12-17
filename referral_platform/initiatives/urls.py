from django.conf.urls import include, url
from django.views.generic import TemplateView
from . import views
from .views import YouthInitiativeView

urlpatterns = [

    # url(r'^youth-led$', YouthInitiativeView.as_view(), name='youth-led'),
    url(
        regex=r'^add/$',
        view=views.AddSubnet.as_view(),
        name='add-initiative'
    ),
    url(
        regex=r'^list/$',
        view=views.YouthInitiativeView.as_view(),
        name='list-initiatives'
    ),

]
