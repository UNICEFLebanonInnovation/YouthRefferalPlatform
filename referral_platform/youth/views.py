from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from referral_platform.users.views import UserRegisteredMixin

from .forms import RegistrationForm
from referral_platform.users.utils import force_default_language


class HomeView(UserRegisteredMixin, TemplateView):

    template_name = 'pages/home.html'


class RegistrationView(LoginRequiredMixin, FormView):

    template_name = 'pages/registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        force_default_language(self.request)
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(RegistrationView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.save(self.request.user)
        return super(RegistrationView, self).form_valid(form)
