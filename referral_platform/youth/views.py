from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from referral_platform.users.views import UserRegisteredMixin

from .forms import RegistrationForm


class HomeView(UserRegisteredMixin, TemplateView):

    template_name = 'pages/home.html'


class RegistrationView(LoginRequiredMixin, FormView):

    template_name = 'pages/registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        form.save(self.request.user)
        return super(RegistrationView, self).form_valid(form)
