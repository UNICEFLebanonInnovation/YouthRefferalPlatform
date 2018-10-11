from __future__ import unicode_literals

from datetime import date
import datetime
import json
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _t
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.urlresolvers import reverse
from model_utils import Choices
from model_utils.models import TimeStampedModel

from referral_platform.partners.models import PartnerOrganization, Center
from referral_platform.youth.models import YoungPerson, Disability
from referral_platform.locations.models import Location
from .utils import generate_hash
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        return '{} - {}'.format(self.name, self.overview)

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


class NewMapping(models.Model):

    type = models.CharField(
        max_length=254,
        blank=True, null=True,
        verbose_name=_('Assessment Type')
    )
    key = models.CharField(
        max_length=254,
        blank=True, null=True,
        verbose_name=_('Key')
    )
    old_value = models.CharField(
        max_length=254,
        blank=True, null=True,
        verbose_name=_('Old Value')
    )
    new_value = models.CharField(
        max_length=254,
        blank=True, null=True,
        verbose_name=_('New Value')
    )


class Registration(TimeStampedModel):

    location = models.CharField(
        max_length=254,
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
        max_length=254,
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
    # disability = models.ForeignKey(
    #     Disability,
    #     blank=True, null=True,
    #     related_name='+',
    #     verbose_name=_('Disability')
    # )
    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comments')
    )

    class Meta:
        ordering = ['pk']
        verbose_name = _("Registration")
        verbose_name_plural = _("Registrations")

    def __unicode__(self):
        return '{} - {}'.format(self.partner_organization, self.youth)

    def get_assessment(self, slug):
        assessment = self.assessmentsubmission_set.filter(assessment__slug=slug).first()
        if assessment:
            return assessment.data
        return '------'

    @property
    def youth_birthday(self):
        return self.youth.birthday

    @property
    def youth_age(self):
        return self.youth.calc_age

    @property
    def youth_bayanati_ID(self):
        return self.youth.bayanati_ID

    @property
    def youth_nationality(self):
        return self.youth.nationality

    @property
    def youth_marital_status(self):
        return self.youth.marital_status

    @property
    def youth_address(self):
        return self.youth.address

    @property
    def registration_assessment(self):
        return self.get_assessment('registration')

    @property
    def pre_civic_engagement(self):
        return self.get_assessment('pre_assessment')

    @property
    def post_civic_engagement(self):
        return self.get_assessment('post_assessment')

    @property
    def initiative_registration(self):
        return self.get_assessment('init_registration')

    @property
    def initiative_implementation(self):
        return self.get_assessment('init_exec')

    @property
    def pre_entrepreneurship(self):
        return self.get_assessment('pre_entrepreneurship')

    @property
    def post_entrepreneurship(self):
        return self.get_assessment('post_entrepreneurship')

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
    status = models.CharField(max_length=254, choices=STATUS, default=STATUS.enrolled)
    data = JSONField(blank=True, null=True, default=dict)
    new_data = JSONField(blank=True, null=True, default=dict)

    def get_data_option(self, column, option):
        column_value = self.data.get(column, '')
        if column_value and option in column_value:
            return 'yes'
        return 'no'

    def update_field(self):

        data = self.data
        assessment_type = self.assessment.slug
        new_data = {}
        for key in data:
            old_value = data[key]
            try:
                 obj = NewMapping.objects.get(type=assessment_type, key=key, old_value=old_value)
                 new_data[key] = obj.new_value
            except Exception as ex:
                new_data[key] = old_value
                continue

        self.new_data = new_data
        self.save()

    post_save.connect(update_field())


class AssessmentHash(models.Model):

    hashed = models.CharField(max_length=254, unique=True)
    registration = models.CharField(max_length=20)
    assessment_slug = models.CharField(max_length=50)
    partner = models.CharField(max_length=5)
    user = models.CharField(max_length=20)
    timestamp = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    @property
    def name(self):
        return '{}{}{}{}{}'.format(
            self.registration,
            self.assessment_slug,
            self.partner,
            self.user,
            self.timestamp,
        )

    def __unicode__(self):
        return '{}-{}-{}-{}-{}-{}'.format(
            self.hashed,
            self.registration,
            self.assessment_slug,
            self.partner,
            self.user,
            self.timestamp,
        )

    def save(self, **kwargs):
        """
        Generate unique Hash for every assessment
        :param kwargs:
        :return:
        """
        if self.pk is None:
            self.hashed = generate_hash(self.name)

        super(AssessmentHash, self).save(**kwargs)
