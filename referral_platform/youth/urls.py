
from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import HomeView, RegistrationView


urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^registration$', RegistrationView.as_view(), name='registration'),
]


