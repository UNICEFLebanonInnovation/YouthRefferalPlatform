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
        return reverse('youth:add')

class PasswordContextMixin(object):
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(PasswordContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        if self.extra_context is not None:
            context.update(self.extra_context)
        return context


class LoginRedirectView(LoginRequiredMixin, RedirectView):
    permanent = True

    def get_redirect_url(self):
        # if has_group(self.request.user, 'ENROL_EDIT'):
        #     return reverse('enrollments:enrollment_edit', kwargs={})
        # if has_group(self.request.user, 'SCHOOL'):
        #     return reverse('enrollments:enrollment_patch', kwargs={})
        # if has_group(self.request.user, 'ALP_SCHOOL'):
        #     return reverse('alp:alp_data_collecting', kwargs={}) + '?1'
        if has_group(self.request.user, 'PARTNER'):
            return reverse('alp:alp_outreach', kwargs={}) + '?'
        if has_group(self.request.user, 'HELPDESK'):
            return reverse('helpdesk_dashboard', kwargs={})
        return reverse('home')


def deprecate_current_app(func):
    """
    Handle deprecation of the current_app parameter of the views.
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if 'current_app' in kwargs:
            warnings.warn(
                "Passing `current_app` as a keyword argument is deprecated. "
                "Instead the caller of `{0}` should set "
                "`request.current_app`.".format(func.__name__),
                RemovedInDjango20Warning
            )
            current_app = kwargs.pop('current_app')
            request = kwargs.get('request', None)
            if request and current_app is not None:
                request.current_app = current_app
        return func(*args, **kwargs)

    return inner


@sensitive_post_parameters()
@csrf_protect
@login_required
@deprecate_current_app
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    warnings.warn("The password_change() view is superseded by the "
                  "class-based PasswordChangeView().",
                  RemovedInDjango21Warning, stacklevel=2)
    if post_change_redirect is None:
        post_change_redirect = reverse('change_password_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@login_required
@deprecate_current_app
def change_password_done(request,
                         template_name='registration/password_change_done.html',
                         extra_context=None):
    warnings.warn("The password_change_done() view is superseded by the "
                  "class-based PasswordChangeDoneView().",
                  RemovedInDjango21Warning, stacklevel=2)
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('change_password_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super(PasswordChangeView, self).form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeDoneView, self).dispatch(*args, **kwargs)
