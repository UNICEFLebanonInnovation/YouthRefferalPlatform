# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import functools
import warnings

from braces.views import UserPassesTestMixin
from django.contrib.auth import (
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, TemplateView, FormView

from referral_platform.users.templatetags.util_tags import has_group
from .models import User
from django.shortcuts import render


class UserRegisteredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self, user):
        return hasattr(user, 'profile')

    def no_permissions_fail(self, request=None):
        return HttpResponseRedirect(reverse('youth:registration'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by email
    slug_field = 'email'
    slug_url_kwarg = 'email'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        if self.request.user.partner:
            return reverse('partners:home',
                           kwargs={'partner': self.request.user.partner})

        return reverse('users:detail',
                       kwargs={'email': self.request.user.email})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'email': self.request.user.email})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'email'


class UserChangeLanguageRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'set_language'

    def get_redirect_url(self, *args, **kwargs):
        user_language = kwargs['language']
        translation.activate(user_language)
        self.request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return reverse('registrations:list', kwargs={})


def user_overview(request):

    model = User
    partner = User.partner
    country = User.country
    username = User.email

    context = {
        'partner': partner,
        'country': country,
        'username': username,
        # 'num_instances_available': num_instances_available,
        # 'num_authors': num_authors,
               }
    return render(request, 'profile.html', context=context)


    # def get_context_data(self, **kwargs):
    #     locations = self.request.user.profile.partner_organization.locations
    #     enrollement = Enrollment.objects.filter(
    #         youth=self.request.user.profile,
    #         course__path=self.object
    #     ).last()
    #     kwargs.update({'enrollment': enrollement, 'locations': locations})
    #     return super(CoursesOverview, self).get_context_data(**kwargs)


# def view_profile(request, pk=None):
#     if pk:
#         user = User.objects.get(pk=pk)
#     else:
#         user = request.user
#     args = {'user': user}
#     return render(request, '/users/profile.html', args)
