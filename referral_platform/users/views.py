# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import UserPassesTestMixin

from .models import User


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
