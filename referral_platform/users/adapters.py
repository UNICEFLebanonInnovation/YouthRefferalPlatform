# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def save_user(self, request, user, form, commit=True):
        """
        Overriding save user to make signup inactive by default
        :param request:
        :param user:
        :param form:
        :param commit:
        :return:
        """
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)
        user.is_active = False
        user.save()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
