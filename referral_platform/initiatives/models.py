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
from django.core.urlresolvers import reverse
from referral_platform.users.models import User
from referral_platform.youth.models import YoungPerson
from referral_platform.partners.models import PartnerOrganization
from referral_platform.locations.models import Location
from referral_platform.registrations.models import Registration, NewMapping, JSONField, Assessment
from .utils import generate_hash
from django.db.models.signals import post_save
from django.dispatch import receiver

class YouthLedInitiative(models.Model):

    def __unicode__(self):
        return '{} - {}'.format(self.title, self.Participants)

    # def __iter__(self):
    #     return iter([self.name,
    #                  self.slug,
    #                  self.overview,
    #                  self.start_date,
    #                  self.end_date,
    #                  self.capacity,
    #                  self.assessment_form,
    #                  self.order,
    #                  self.partner])

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

    SKILL_AREAS = Choices(
        ('self-management', _('Self-Management')),
        ('teamwork', _('Cooperation & Teamwork')),
        ('creativity', _('Creativity')),
        ('critical_thinking', _('Critical Thinking')),
        ('negotiation', _('Negotiation')),
        ('diversity', _('Respect for diversity')),
        ('decision_making', _('Decision Making')),
        ('participation', _('Participation')),
        ('communication', _('Communication')),
        ('empathy', _('Empathy')),
        ('problem_solving', _('Problem-Solving')),
        ('resilience', _('Resilience')),
    )

    RESOURCE_TYPES = Choices(
        ('financial', _('Financial (self-explanatory)')),
        ('technical', _('Technical (for ex. developing awareness tools materials, trainings..etc)')),
        ('in-kind', _('In-Kind (posters, booklet,etc)')),
    )

    title = models.CharField(max_length=255, verbose_name=_('Initiative Title'))
    location = models.ForeignKey(Location, blank=True, null=True, verbose_name="Initiative Location")
    partner_organization = models.ForeignKey(PartnerOrganization, blank=True, null=True, verbose_name="Partner Organization")
    # members = models.ManyToManyField(YoungPerson, blank=True, )
    Participants = models.ManyToManyField(Registration, related_name='+', blank=True, null=True, verbose_name=_('Participants'))

    # start_date = models.DateField(blank=True, null=True)
    duration = models.CharField(
        max_length=254,
        verbose_name=_('Duration of the initiative'),
        blank=True, null=True,
        choices=Choices(
            ('1_2', _('1-2 weeks')),
            ('3_4', _('3-4 weeks')),
            ('4_6', _('4-6 weeks')),
            ('6_plus', _('More than 6 weeks')),

        )
    )

    type = models.CharField(
        max_length=254,
        blank=True,
        verbose_name=_('Initiative Types'),
        null=True,
        choices=Choices(
                ('basic services', _('Basic Services')),
                ('social Cohesion', _('Social cohesion')),
                ('environmental', _('Environmental')),
                ('health services', _('Health Services')),
                ('protection', _('Protection')),
                ('advocacy', _('Advocacy or Raising awareness')),
                ('political', _('Political')),
                ('religious and spiritual', _('Spiritual/Religious')),
                ('sports', _('Sports')),
                ('economic art cultural', _('Economic art cultural')),
                ('educational', _('educational')),
                ('other', _('Other'))
        )

    )
    # type = MultiSelectField(choices=INITIATIVE_TYPES)


    # knowledge_areas = models.CharField(
    #         choices=SKILL_AREAS,
    #         max_length=254,
    #         blank=True,
    #         null=True,
    #     ),
    #
    # why_this_initiative = models.TextField(blank=True, null=True)

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
    sex_of_beneficiaries = models.CharField(
        max_length=254,
        blank=True, null=True,
        choices=Choices(
            ('both', _('Both male and females')),
            ('male', _('Only males')),
            ('female', _('only female')),
        )
    )
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
    #
    # resources_type = models.CharField(
    #     max_length=254,
    #     blank=True, null=True,
    #     choices=RESOURCE_TYPES
    # )
    #
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

    def get_assessment(self, slug):
        assessment = self.assessmentsubmission_set.filter(assessment__slug=slug).first()
        if assessment:
            return assessment.data
        return '------'

    @property
    def initiative_registration(self):
        return self.get_assessment('init_registration')

    @property
    def initiative_implementation(self):
        return self.get_assessment('init_exec')

    def get_absolute_url(self):
        return reverse('initiatives:edit', kwargs={'pk': self.id})


class AssessmentSubmission(models.Model):
    STATUS = Choices(
        'enrolled',
        'pre_test',
        'post_test'
    )

    initiative = models.ForeignKey(YouthLedInitiative, null=True)
    assessment = models.ForeignKey(Assessment, related_name='+')
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

    # def save(self, **kwargs):
    #     """
    #     Generate unique Hash for every assessment
    #     :param kwargs:
    #     :return:
    #     """
    #     if self.pk:
    #         self.update_field()
    #
    #     super(AssessmentSubmission, self).save(**kwargs)


# class AssessmentHash(models.Model):
#
#     hashed = models.CharField(max_length=254, unique=True)
#     registration = models.CharField(max_length=20)
#     assessment_slug = models.CharField(max_length=50)
#     partner = models.CharField(max_length=5)
#     user = models.CharField(max_length=20)
#     timestamp = models.CharField(max_length=100)
#     title = models.CharField(max_length=254)
#     type = models.CharField(max_length=254)
#     location = models.CharField(max_length=254)
#
#     class Meta:
#         ordering = ['id']
#
#     @property
#     def name(self):
#         return '{}{}{}{}{}'.format(
#             self.registration,
#             self.assessment_slug,
#             self.partner,
#             self.user,
#             self.timestamp,
#             self.title,
#             self.type,
#             self.location,
#         )
#
#     def __unicode__(self):
#         return '{}-{}-{}-{}-{}-{}'.format(
#             self.hashed,
#             self.registration,
#             self.assessment_slug,
#             self.partner,
#             self.user,
#             self.timestamp,
#             self.title,
#             self.type,
#             self.location,
#         )
#
#     def save(self, **kwargs):
#         """
#         Generate unique Hash for every assessment
#         :param kwargs:
#         :return:
#         """
#         if self.pk is None:
#             self.hashed = generate_hash(self.name)
#
#         super(AssessmentHash, self).save(**kwargs)
