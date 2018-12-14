from __future__ import unicode_literals, absolute_import, division

from datetime import date
import datetime

# from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel

from referral_platform.users.models import User
from referral_platform.youth.models import YoungPerson
from referral_platform.partners.models import PartnerOrganization
from referral_platform.locations.models import Location


class YouthLedInitiative(models.Model):

    INITIATIVE_TYPES = Choices(
        ('basic_services', _('Improving or installing basic services (electricity, water, sanitation, and waste removal)')),
        ('social', _('Enhancing social cohesion')),
        ('environmental', _('Environmental')),
        ('health_services', _('Health Services')),
        ('informational', _('Educational, informational or knowledge sharing')),
        ('advocacy', _('Advocacy or Raising awareness')),
        ('political', _('Political')),
        ('religious', _('Spiritual/Religious')),
        ('culture', _('Artistic/Cultural/Sports')),
        ('safety', _('Enhancing public safety')),
        ('public_spaces', _('Improving Public Spaces (parks, hospitals, buildings, schools, sidewalks)')),
        ('other', _('Other')),
    )

    # SKILL_AREAS = Choices(
    #     ('self-management', _('Self-Management')),
    #     ('teamwork', _('Cooperation & Teamwork')),
    #     ('creativity', _('Creativity')),
    #     ('critical_thinking', _('Critical Thinking')),
    #     ('negotiation', _('Negotiation')),
    #     ('diversity', _('Respect for diversity')),
    #     ('decision_making', _('Decision Making')),
    #     ('participation', _('Participation')),
    #     ('communication', _('Communication')),
    #     ('empathy', _('Empathy')),
    #     ('problem_solving', _('Problem-Solving')),
    #     ('resilience', _('Resilience')),
    # )
    #
    # RESOURCE_TYPES = Choices(
    #     ('financial', _('Financial (self-explanatory)')),
    #     ('technical', _('Technical (for ex. developing awareness tools materials, trainings..etc)')),
    #     ('in-kind', _('In-Kind (posters, booklet,etc)')),
    # )

    title = models.CharField(max_length=255)
    location = models.ForeignKey(Location, blank=True, null=True)
    partner_organization = models.ForeignKey(PartnerOrganization, blank=True, null=True)
    members = models.ManyToManyField(YoungPerson, blank=True)

    # start_date = models.DateField(blank=True, null=True)
    duration = models.CharField(
        max_length=254,
        blank=True, null=True,
        choices=Choices(
            ('1_2', _('1-2 weeks')),
            ('3_4', _('3-4 weeks')),
            ('4_6', _('4-6 weeks')),
            ('6_plus', _('More than 6 weeks')),

        )
    )

    initiative_types = models.CharField(
            choices=INITIATIVE_TYPES,
            max_length=254,
            blank=True,
            null=True,
        ),

    # knowledge_areas = models.CharField(
    #         choices=SKILL_AREAS,
    #         max_length=254,
    #         blank=True,
    #         null=True,
    #     ),

    # why_this_initiative = models.TextField(blank=True, null=True)
    #
    # other_groups = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('ngos', _('Other NGOs')),
    #         ('schools', _('Schools')),
    #         ('municipality', _('Municipality')),
    #         ('other', _('Other')),
    #     ),
    # )
    #
    # number_of_beneficiaries = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('1-50', _('1-50')),
    #         ('51-100 ', _('51-100')),
    #         ('501-1000', _('501-1000')),
    #         ('1000-plus', _('greater than 1000')),
    #     )
    # )
    # age_of_beneficiaries = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('1-6', _('1-6 years')),
    #         ('7-13', _('7-13 years')),
    #         ('14-24', _('14-24 years')),
    #         ('25-50', _('25-50 years')),
    #         ('50-plus', _('50 years and above')),
    #     )
    # )
    # sex_of_beneficiaries = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('both', _('Both male and females')),
    #         ('male', _('Only males')),
    #         ('female', _('only female')),
    #     )
    # )
    # indirect_beneficiaries = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('1-50', _('1-50')),
    #         ('51-100 ', _('51-100')),
    #         ('501-1000', _('501-1000')),
    #         ('1000-plus', _('greater than 1000')),
    #     )
    # )
    # needs_resources = models.BooleanField(default=False)
    # resources_from = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('unicef', _('UNICEF')),
    #         ('local ', _('Local Business')),
    #         ('organization', _('Organisation')),
    #     )
    # )

    # resources_type = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=RESOURCE_TYPES
    # )

    # description = models.TextField(blank=True, null=True)
    # planned_results = models.TextField(blank=True, null=True)
    # anticpated_challenges = models.TextField(blank=True, null=True)
    # mitigation_of_challenges = models.TextField(blank=True, null=True)
    # how_to_measure_progress = models.TextField(blank=True, null=True)
    # how_to_ensure_sustainability = models.TextField(blank=True, null=True)
    #
    # team_participation_rating = models.CharField(
    #     max_length=100,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('excellent', _('Excellent - All of our team members were committed to the initiative')),
    #         ('good', _('Good - Most of our team was committed to the initiative')),
    #         ('low', _('Low - Some team members stopped participating')),
    #     )
    # )
    #
    # initiative_activities = ArrayField(
    #     models.CharField(
    #         choices=INITIATIVE_TYPES,
    #         max_length=254,
    #         blank=True,
    #         null=True,
    #     ),
    #     blank=True,
    #     null=True,
    # )
    #
    # number_of_beneficiaries_reached = models.CharField(
    #     max_length=100,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('exceeded', _('Exceeded the total number of direct beneficiaries that we planned to reach (greater than 100%)')),
    #         ('reached', _('Reached all of the direct beneficiaries planned (100%)')),
    #         ('half', _('Reached more than half of the direct beneficiaries planned (50% or more)')),
    #         ('less', _('Reached less than half of the direct beneficiaries planned (Less then 49%)" (50% or more)')),
    #     )
    # )
    # mentor = models.NullBooleanField()
    # mentor_was_helpful = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('yes', _('Yes')),
    #         ('no', _('No')),
    #         ('somewhat', _('Somewhat')),
    #     )
    # )
    # support_helpful = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=Choices(
    #         ('yes', _('Yes')),
    #         ('no', _('No')),
    #         ('somewhat', _('Somewhat')),
    #     )
    # )
    # challenges_face = models.TextField(blank=True, null=True)
    # lessons_learnt = models.TextField(blank=True, null=True)
