from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.urlresolvers import reverse

from model_utils import Choices
from model_utils.models import TimeStampedModel

from referral_platform.partners.models import PartnerOrganization, Center
from referral_platform.youth.models import YoungPerson, Disability, EducationLevel
from referral_platform.locations.models import Location


class Assessment(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    overview = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    assessment_form = models.URLField(blank=True, null=True)
    order = models.TextField(blank=False, null=False, default=1)
    partner = models.ForeignKey(PartnerOrganization, null=True, blank=True,)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.overview

    def __iter__(self):
        return iter([self.name,
                     self.slug,
                     self.overview,
                     self.start_date,
                     self.end_date,
                     self.capacity,
                     self.assessment_form,
                     self.order,
                     self.partner])


class Registration(TimeStampedModel):

    location = models.CharField(
        max_length=50,
        blank=True, null=True,
        verbose_name=_('Location')
    )
    partner_organization = models.ForeignKey(
        PartnerOrganization,
        blank=True, null=True,
        related_name='+',
        verbose_name=_('Partner organization'),
    )
    governorate = models.ForeignKey(
        Location,
        blank=True, null=True,
        related_name='+',
        verbose_name=_('Governorate')
    )
    center = models.ForeignKey(
        Center,
        blank=True, null=True,
        related_name='+',
        verbose_name=_('Center')
    )
    trainer = models.CharField(
        max_length=50,
        blank=True, null=True,
        verbose_name=_('Trainer')
    )
    youth = models.ForeignKey(
        YoungPerson,
        related_name='registrations',
        blank=False, null=False,
        verbose_name=_('Youth'),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False, null=True,
        related_name='+',
        verbose_name=_('Created by')
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        related_name='+',
        verbose_name=_('Modified by'),
    )

    class Meta:
        ordering = ['pk']
        verbose_name = _("Registration")
        verbose_name_plural = _("Registrations")

    def get_absolute_url(self):
        return reverse('registrations:edit', kwargs={'pk': self.id})


class AssessmentSubmission(models.Model):

    STATUS = Choices(
        'enrolled',
        'pre_test',
        'post_test'
    )

    registration = models.ForeignKey(Registration)
    youth = models.ForeignKey(YoungPerson)
    assessment = models.ForeignKey(Assessment)
    status = models.CharField(max_length=50, choices=STATUS, default=STATUS.enrolled)
    data = JSONField(blank=True, null=True, default=dict)