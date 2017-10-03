from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import ArrayField, JSONField

from model_utils import Choices
from model_utils.models import TimeStampedModel

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

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class AssessmentSubmission(models.Model):

    STATUS = Choices(
        'enrolled',
        'pre_test',
        'post_test'
    )

    youth = models.ForeignKey(YoungPerson)
    assessment = models.ForeignKey(Assessment)
    status = models.CharField(max_length=50, choices=STATUS, default=STATUS.enrolled)
    data = JSONField(blank=True, null=True, default=dict)


class CLM(TimeStampedModel):

    LANGUAGES = Choices(
        ('english_arabic', _('English/Arabic')),
        ('french_arabic', _('French/Arabic'))
    )
    STATUS = Choices(
        'enrolled',
        'pre_test',
        'post_test'
    )
    YES_NO = Choices(
        (1, _("Yes")),
        (0, _("No"))
    )
    REFERRAL = Choices(
        ('from_same_ngo', _('Referral from the same NGO')),
        ('from_other_ngo', _('Referral from an other NGO')),
        ('form_official_reference', _('Referral from an official reference (Mukhtar, Municipality, School Director, etc.)')),
        ('from_host_community', _('Referral from the host community')),
        ('from_displaced_community', _('Referral from the displaced community')),
    )
    PARTICIPATION = Choices(
        ('less_than_5days', _('Less than 5 absence days')),
        ('5_10_days', _('5 to 10 absence days')),
        ('10_15_days', _('10 to 15 absence days')),
        ('more_than_15days', _('More than 15 absence days'))
    )
    BARRIERS = Choices(
        ('seasonal_work', _('Seasonal work')),
        ('transportation', 'Transportation'),
        ('weather', _('Weather')),
        ('sickness', _('Sickness')),
        ('security', _('Security')),
        ('other', _('Other'))
    )
    HAVE_LABOUR = Choices(
        ('no', _('No')),
        ('yes_morning', _('Yes - Morning')),
        ('yes_afternoon', _('Yes - Afternoon')),
    )
    LABOURS = Choices(
        ('agriculture', _('Agriculture')),
        ('building', _('Building')),
        ('manufacturing', _('Manufacturing')),
        ('retail_store', _('Retail / Store')),
        ('begging', _('Begging')),
        ('other_many_other', _('Other (hotel, restaurant, transport, personal services such as cleaning, hair care, cooking and childcare)')),
        ('other', _('Other')),
    )
    LEARNING_RESULT = Choices(
        ('graduated_next_level', _('Graduated to the next level')),
        ('graduated_to_formal_kg', _('Graduated to formal education - KG')),
        ('graduated_to_formal_level1', _('Graduated to formal education - Level 1')),
        ('referred_to_another_program', _('Referred to another program')),
        ('dropout', _('Dropout from school'))
    )
    governorate = models.ForeignKey(
        Location,
        blank=True, null=True,
        related_name='+',
    )
    district = models.ForeignKey(
        Location,
        blank=True, null=True,
        related_name='+',
    )
    location = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    language = ArrayField(
        models.CharField(
            choices=LANGUAGES,
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    student = models.ForeignKey(
        YoungPerson,
        blank=False, null=True,
        related_name='+',
    )
    disability = models.ForeignKey(
        Disability,
        blank=True, null=True,
        related_name='+',
    )
    have_labour = ArrayField(
        models.CharField(
            choices=HAVE_LABOUR,
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    labours = ArrayField(
        models.CharField(
            choices=LABOURS,
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    labour_hours = models.IntegerField(
        blank=True,
        null=True,
    )
    hh_educational_level = models.ForeignKey(
        EducationLevel,
        blank=True, null=True,
        related_name='+',
    )

    status = models.CharField(max_length=50, choices=STATUS, default=STATUS.enrolled)
    pre_test = JSONField(blank=True, null=True)
    post_test = JSONField(blank=True, null=True)

    scores = JSONField(blank=True, null=True, default=dict)

    participation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=PARTICIPATION
    )
    barriers = ArrayField(
        models.CharField(
            choices=BARRIERS,
            max_length=100,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    learning_result = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=LEARNING_RESULT
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False, null=True,
        related_name='+',
    )
    deleted = models.BooleanField(blank=True, default=False)
    dropout_status = models.BooleanField(blank=True, default=False)
    moved = models.BooleanField(blank=True, default=False)
    outreach_barcode = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    new_registry = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=YES_NO,
    )
    student_outreached = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=YES_NO,
    )
    have_barcode = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=YES_NO,
    )
    registration_date = models.DateField(
        blank=True,
        null=True,
    )

    @property
    def student_fullname(self):
        if self.student:
            return self.student.full_name
        return ''

    @property
    def student_age(self):
        if self.student:
            return self.student.age
        return 0

    def get_absolute_url(self):
        return '/youth/edit/%d/' % self.pk

    def __unicode__(self):
        if self.student:
            return self.student.__unicode__()
        return str(self.id)

    class Meta:
        abstract = True

