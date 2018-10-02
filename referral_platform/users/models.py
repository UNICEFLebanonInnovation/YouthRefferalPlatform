# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from referral_platform.partners.models import PartnerOrganization
from referral_platform.locations.models import Location

from .managers import UserManager


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), blank=True, max_length=255)
    last_name = models.CharField(_('last name'), blank=True, max_length=255)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    partner = models.ForeignKey(
        PartnerOrganization,
        null=True, blank=True
    )
    country = models.ForeignKey(
        Location,
        null=True, blank=True,
    ).filter(location__type='Country')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        pass
        '''
        Sends an email to this User.
        '''
        # send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'email': self.email})
