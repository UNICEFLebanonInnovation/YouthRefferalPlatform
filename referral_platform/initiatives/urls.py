from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import YouthInitiativeView

urlpatterns = [

    url(r'^youth-led$', YouthInitiativeView.as_view(), name='youth-led'),

]
