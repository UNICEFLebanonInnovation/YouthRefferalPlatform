from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils.translation import ugettext as _
from model_utils import Choices
from django.core.urlresolvers import reverse
from referral_platform.partners.models import PartnerOrganization
from referral_platform.locations.models import Location
from referral_platform.registrations.models import Registration, NewMapping, Assessment
from multiselectfield import MultiSelectField


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

    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Initiative Title'))
    governorate = models.ForeignKey(Location, blank=True, null=True, verbose_name="Governorate")
    partner_organization = models.ForeignKey(PartnerOrganization, blank=True, null=True, verbose_name="Partner Organization")
    Participants = models.ManyToManyField(Registration, related_name='+', verbose_name=_('Participants'))

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

    type = MultiSelectField(choices=INITIATIVE_TYPES)

    @property
    def get_participants(self):
        return "\n".join([str(p.id) for p in self.Participants.all()])

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

    @property
    def initiative_post_civic(self):
        return self.get_assessment('init_post_civic')

    def get_absolute_url(self):
        return reverse('initiatives:edit', kwargs={'pk': self.id})

    def __unicode__(self):
        return '{} - {}'.format(self.title, self.Participants)


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
