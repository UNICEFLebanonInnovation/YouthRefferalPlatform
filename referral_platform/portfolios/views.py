from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/home.html'


class RegistrationView(LoginRequiredMixin, FormView):

    template_name = 'pages/registration.html'
    form_class = RegistrationForm

