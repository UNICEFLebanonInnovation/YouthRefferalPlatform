from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils.translation import ugettext as _

from model_utils import Choices

from referral_platform.students.models import Person


class OutreachYear(models.Model):
    name = models.CharField(max_length=100, unique=True)
    current_year = models.BooleanField(blank=True, default=False)

    class Meta:
        ordering = ['name']
        verbose_name = "Outreach Year"

    def __unicode__(self):
        return self.name


class HouseHold(models.Model):

    interview_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('1', _('Granted')),
            ('2', _('Denied')),
            ('3', _('Granted for the referral')),
        )
    )
    interview_comment = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=45, blank=True, null=True)
    residence_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('1', _('Informal Settlement')),
            ('2', _('House or Apartment')),
            ('3', _('Garage, Store or other')),
        )
    )
    p_code = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    number_of_children = models.CharField(max_length=45, blank=True, null=True)
    barcode_number = models.CharField(max_length=45, blank=True, null=True)

    social_worker_name = models.CharField(max_length=200, blank=True, null=True)
    partner_name = models.CharField(max_length=200, blank=True, null=True)
    governorate = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    village = models.CharField(max_length=200, blank=True, null=True)
    interview_date = models.CharField(max_length=200, blank=True, null=True)

    children = JSONField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.name


class Child(Person):

    household = models.ForeignKey(
        HouseHold,
        blank=True, null=True,
        related_name='+'
    )

    barcode_subset = models.CharField(max_length=45, blank=True, null=True)
    current_situation = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('1', _('Education system 1')),
            ('2', _('Education system 2')),
            ('3', _('Education system 3')),
            ('4', _('Education system 4')),
            ('5', _('Education system 5')),
            ('6', _('Education system 6')),
            ('7', _('Education system 7')),
        )
    )
    last_education_year = models.CharField(max_length=45, blank=True, null=True)
    last_public_school_location = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('Leb', _('Lebanon')),
            ('Syr', _('Syria')),
            ('Irq', _('Iraq')),
            ('Other', _('Other')),
        )
    )
    last_informal_education = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('ALP', _('ALP')),
            ('BLN', _('BLN')),
            ('CB-ECE', _('CB-ECE')),
            ('SALP', _('SALP')),
            ('Prep.ALP', _('Prep.ALP')),
            ('Special_EDU_Dis', _('Special_EDU_Dis')),
        )
    )
    not_enrolled_reasons = ArrayField(
        models.CharField(
            choices=Choices(
                ('1', _('Reason 1')),
                ('2', _('Reason 2')),
                ('3', _('Reason 3')),
                ('4', _('Reason 4')),
                ('5', _('Reason 5')),
                ('6', _('Reason 6')),
                ('7', _('Reason 7')),
                ('8', _('Reason 8')),
                ('9', _('Reason 9')),
                ('10', _('Reason 10')),
                ('11', _('Reason 11')),
                ('12', _('Reason 12')),
                ('13', _('Reason 13')),
                ('14', _('Reason 14')),
                ('15', _('Reason 15')),
                ('16', _('Reason 16')),
                ('17', _('Reason 17')),
                ('18', _('Reason 18')),
            ),
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )

    consent_child_protection = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('Yes', _('Yes')),
            ('No', _('No')),
        )
    )
    work_type = models.CharField(max_length=100, blank=True, null=True)
    disability_type = ArrayField(
        models.CharField(
            choices=Choices(
                ('Walking', _('Walking')),
                ('Seeing', _('Seeing')),
                ('Hearing', _('Hearing')),
                ('Speaking', _('Speaking')),
                ('Self_Care', _('Self Care')),
                ('Learning', _('Learning')),
                ('Interacting', _('Interacting')),
                ('Other', _('Other')),
            ),
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    disability_note = models.CharField(max_length=100, blank=True, null=True)
    other_disability_note = models.CharField(max_length=100, blank=True, null=True)
    disability_comments = models.CharField(max_length=200, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    retention_support = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('1', _('Retention Support 1')),
            ('2', _('Retention Support 2')),
            ('3', _('Retention Support 3')),
            ('4', _('Retention Support 4')),
            ('5', _('Retention Support 5')),
            ('6', _('Retention Support 6')),
        )
    )
    formal_education_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('1', _('Formal education 1')),
            ('2', _('Formal education 2')),
            ('3', _('Formal education 3')),
            ('4', _('Formal education 4')),
        )
    )
    formal_education_shift = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('KG', _('KG')),
            ('First', _('First shift')),
            ('Second', _('Second shift')),
            ('ECE', _('ECE')),
            ('TVET', _('TVET')),
        )
    )
    informal_education_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices(
            ('ALP', _('ALP')),
            ('BLN', _('BLN')),
            ('CBECE', _('CB-ECE')),
            ('SALP', _('SALP')),
        )
    )
    referred_school = models.CharField(max_length=200, blank=True, null=True)
    referred_org = models.CharField(max_length=200, blank=True, null=True)
    referred_school_name = models.CharField(max_length=200, blank=True, null=True)
    referred_org_name = models.CharField(max_length=200, blank=True, null=True)
    referral_reason = ArrayField(
        models.CharField(
            choices=Choices(
                ('ALP', _('ALP')),
                ('BLN', _('BLN')),
                ('CBECE', _('CB-ECE')),
                ('SALP', _('SALP')),
            ),
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    referral_note = models.CharField(max_length=200, blank=True, null=True)
