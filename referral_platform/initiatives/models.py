from __future__ import unicode_literals, absolute_import, division

from datetime import date
import datetime

from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

from referral_platform.users.models import User
from referral_platform.portfolios.models import YoungPerson
from referral_platform.partners.models import PartnerOrganization
from referral_platform.locations.models import Location


class YouthLedInitiative(models.Model):


    title = models.CharField(max_length=255)
    location = models.ForeignKey(Location, blank=True, null=True)
    partner_organization = models.ForeignKey(PartnerOrganization, blank=True, null=True)
    members = models.ManyToManyField(YoungPerson, blank=True, null=True)

    start_date = models.DateField(blank=True, null=True)
    duration = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=Choices(
            ('1_2', _('1-2 weeks')),
            ('3_4', _('3-4 weeks')),
            ('4_6', _('4-6 weeks')),
            ('6_plus', _('More than 6 weeks')),

        )
    )

    initiative_type = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )

    knowledge_areas = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    why_this_initiative = models.TextField(blank=True, null=True)

    number_of_beneficiaries = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=Choices(
            ('1-50', _('1-50')),
            ('51-100 ', _('51-100')),
            ('501-1000', _('501-1000')),
            ('1000-plus', _('greater than 1000')),
        )
    )
    age_of_beneficiaries = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=Choices(
            ('1-6', _('1-6 years')),
            ('7-13', _('7-13 years')),
            ('14-24', _('14-24 years')),
            ('25-50', _('25-50 years')),
            ('50-plus', _('50 years and above')),
        )
    )
    sex_of_beneficiaries = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=Choices(
            ('both', _('Both male and females')),
            ('male', _('Only males')),
            ('female', _('only female')),
        )
    )
    indirect_beneficiaries = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=Choices(
            ('1-50', _('1-50')),
            ('51-100 ', _('51-100')),
            ('501-1000', _('501-1000')),
            ('1000-plus', _('greater than 1000')),
        )
    )
    needs_resources = models.BooleanField(default=False)
    resources_from = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=Choices(
            ('unicef', _('UNICEF')),
            ('local ', _('Local Business')),
            ('organization', _('Organisation')),
        )
    )
    resources_type = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=Choices(
            ('financial', _('Financial (self-explanatory)')),
            ('technical', _('Technical (for ex. developing awareness tools materials, trainings..etc)')),
            ('in-kind', _('In-Kind (posters, booklet,etc)')),
        )
    )

    description = models.TextField(blank=True, null=True)
    planned_results = models.TextField(blank=True, null=True)
    anticpated_challenges = models.TextField(blank=True, null=True)
    mitigation_of_challenges = models.TextField(blank=True, null=True)
    how_to_measure_progress = models.TextField(blank=True, null=True)
    how_to_ensure_sustainability = models.TextField(blank=True, null=True)
