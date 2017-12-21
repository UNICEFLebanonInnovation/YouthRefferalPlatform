from __future__ import unicode_literals, absolute_import, division

from datetime import date
import datetime

from django.contrib.gis.db import models
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from model_utils import Choices
from model_utils.models import TimeStampedModel

from referral_platform.users.models import User
from referral_platform.partners.models import PartnerOrganization, Center
from referral_platform.locations.models import Location
from .utils import *


class Nationality(models.Model):
    name = models.CharField(max_length=45, unique=True, verbose_name=_('Nationality'))
    code = models.CharField(max_length=45, null=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = _("Nationalities")

    def __unicode__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class IDType(models.Model):
    name = models.CharField(max_length=45, unique=True)
    inuse = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
        verbose_name = _("ID Type")
        verbose_name_plural = _("ID Type")

    def __unicode__(self):
        return self.name


class EducationLevel(models.Model):
    name = models.CharField(max_length=45, unique=True)
    note = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = _("ALP Level")
        verbose_name_plural = _("ALP Level")

    def __unicode__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=45, unique=True)

    def __unicode__(self):
        return self.name


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Disability(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Person(TimeStampedModel):
    MONTHS = Choices(
        ('1', _('January')),
        ('2', _('February')),
        ('3', _('March')),
        ('4', _('April')),
        ('5', _('May')),
        ('6', _('June')),
        ('7', _('July')),
        ('8', _('August')),
        ('9', _('September')),
        ('10', _('October')),
        ('11', _('November')),
        ('12', _('December')),
    )

    GENDER = Choices(
        ('', _('Gender')),
        ('male', _('Male')),
        ('female', _('Female')),
    )
    arabic_validator = RegexValidator(r'^[\u0600-\u065F\u066E-\u06FF ]*$', _('Only Arabic characters are allowed.') )

    first_name = models.CharField(max_length=75, validators=[arabic_validator], verbose_name=_('first name'))
    last_name = models.CharField(max_length=75, validators=[arabic_validator], verbose_name=_('last name'))
    father_name = models.CharField(max_length=75, validators=[arabic_validator], verbose_name=_('Father Name'))
    full_name = models.CharField(max_length=225, blank=True, null=True, verbose_name=_('full name'))
    mother_fullname = models.CharField(max_length=255, blank=True, null=True)
    mother_firstname = models.CharField(max_length=75, blank=True, null=True)
    mother_lastname = models.CharField(max_length=75, blank=True, null=True)
    sex = models.CharField(
        max_length=50,
        choices=GENDER,
        verbose_name=_('Gender')
    )
    from datetime import datetime

    current_year = datetime.today().year
    birthday_year = models.CharField(
        max_length=4,
        blank=False,
        null=False,
        choices=((str(x), x) for x in range(current_year - 26, current_year - 6)),
        verbose_name=_('birthday year'),
        default=current_year - 26
    )
    birthday_month = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        default=0,
        choices=MONTHS,
        verbose_name=_('birthday month')
    )
    birthday_day = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        default=0,
        choices=((str(x), x) for x in range(1, 32)),
        verbose_name=_('birthday day')
    )
    age = models.CharField(max_length=4, blank=True, null=True, verbose_name=_('age'))
    phone = models.CharField(max_length=64, blank=True, null=True)
    phone_prefix = models.CharField(max_length=10, blank=True, null=True)
    id_number = models.CharField(max_length=45, blank=True, null=True)
    id_type = models.ForeignKey(
        IDType,
        blank=True,
        null=True
    )
    nationality = models.ForeignKey(
        Nationality,
        related_name='+',
        verbose_name=_('Nationality')
    )
    mother_nationality = models.ForeignKey(
        Nationality,
        blank=True, null=True,
        related_name='+'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('address')
    )
    number = models.CharField(max_length=45, blank=True, null=True)

    def __unicode__(self):
        if not self.first_name:
            return 'No name'

        return u'{} {} {}'.format(
            self.first_name,
            self.father_name,
            self.last_name,
        )

    def nationality_name(self):
        if self.nationality:
            return self.nationality.name

        return ''

    @property
    def birthday(self):
        return u'{}/{}/{}'.format(
            self.birthday_day,
            self.birthday_month,
            self.birthday_year,
        )

    def get_age(self):
        if self.age:
            return self.age
        current_year = datetime.datetime.now().year
        return int(current_year) - int(self.birthday_year)

    @property
    def calc_age(self):
        current_year = datetime.datetime.now().year
        if self.birthday_year:
            return int(current_year) - int(self.birthday_year)
        return 0

    @property
    def calculate_age(self):
        today = date.today()
        years_difference = today.year - int(self.birthday_year)
        is_before_birthday = (today.month, today.day) < (int(self.birthday_month), int(self.birthday_day))
        elapsed_years = years_difference - int(is_before_birthday)
        return elapsed_years

    class Meta:
        abstract = True

    def save(self, **kwargs):
        """
        Generate unique IDs for every person
        :param kwargs:
        :return:
        """
        if self.pk is None:
            self.number = generate_id(
                self.first_name,
                self.father_name,
                self.last_name,
                self.sex,
                self.birthday_day,
                self.birthday_month,
                self.birthday_year,
                self.mother_fullname if self.mother_fullname else ""
            )

        super(Person, self).save(**kwargs)


class YoungPerson(Person):
    MARITAL_STATUS = Choices(
        ('', _('Marital status')),
        ('married', _('Married')),
        ('engaged', _('Engaged')),
        ('divorced', _('Divorced')),
        ('widower', _('Widower')),
        ('single', _('Single')),
    )

    # user = models.OneToOneField(User, related_name='profile')
    parents_phone_number = models.CharField(max_length=64, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Location'))
    partner_organization = models.ForeignKey(PartnerOrganization, blank=True, null=True)
    governorate = models.ForeignKey(Location, verbose_name=_('Governorate'), default='39')
    center = models.ForeignKey(Center, blank=True, null=True)
    disability = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(
        max_length=50,
        choices=MARITAL_STATUS,
        blank=False, null=False,
        verbose_name=_('Marital status'),
        default='single'
    )

    trainer = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Trainer'))

    #bayanati_ID_validator = RegexValidator(r'^[0-9]{6}$', _('Bayanati ID should be composed of exactly 6 numbers .'))
    bayanati_ID = models.CharField(
        max_length=50,
        #validators=[bayanati_ID_validator],
        blank=True, null=True,
        verbose_name=_('Bayanati ID')
    )
    education_status = models.CharField(
        max_length=50,
        choices=Choices(
            ('currently_studying', _('Yes, I am currently studying')),
            ('stopped_studying', _('Yes, but I stopped studying')),
            ('never_studied', _('Never been to an educational institution')),
            ('na', _('NA')),
        ),
        blank=True, null=True
    )
    education_type = models.CharField(
        max_length=50,
        choices=Choices(
            ('non-formal', _('Non formal Education')),
            ('formal', _('Formal Education')),
        ),
        blank=True,
        null=True,
    )
    education_level = models.ForeignKey(EducationLevel, blank=True, null=True)
    education_grade = models.ForeignKey(Grade, blank=True, null=True)
    leaving_education_reasons = ArrayField(
        models.CharField(
            max_length=200,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )

    employment_status = models.CharField(
        max_length=50,
        choices=Choices(
            ('full_time', _('Currently Working - full time')),
            ('part_time', _('Currently Working - part time')),
            ('summer_only', _('Work in Summer Only')),
            ('unemployed', _('Currently Unemployed')),
            ('never_worked', _('Never worked')),
            ('looking_for_work', _('Looking for a work')),
        ),
        blank=True,
        null=True,
    )
    employment_sectors = ArrayField(
        models.CharField(
            max_length=200,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    looking_for_work = models.NullBooleanField()
    through_whom = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    obstacles_for_work = ArrayField(
        models.CharField(
            max_length=200,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    supporting_family = models.NullBooleanField()
    household_composition = ArrayField(
        models.CharField(
            max_length=200,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    household_working = models.IntegerField(
        blank=True,
        null=True,
    )
    safety = models.CharField(
        max_length=50,
        choices=Choices(
            ('safe', _(' I always feel totally safe in my community ')),
            ('mostly_safe', _('Most of the days I feel safe in my community')),
            ('mostly_unsafe', _("Most of the days I don't feel safe in my community ")),
            ('unsafe', _('I never feel safe in my community')),
        ),
        blank=True,
        null=True,
    )
    safety_reasons = ArrayField(
        models.CharField(
            max_length=200,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )

    trained_before = models.BooleanField(default=False)
    not_trained_reason = models.CharField(
        max_length=50,
        choices=Choices(
            ('no_interest', _('No Interest')),
            ('no_money', _('Financial barrier')),
            ('family_pressure', _("Family pressure")),
            ('discrimination', _('Discrimination')),
            ('disability', _('Disability')),
            ('distance', _('Distance')),
            ('safety', _('Safety')),
        ),
        blank=True,
        null=True,
    )

    sports_group = models.BooleanField(default=False)
    sport_type = models.ForeignKey(Sport, blank=True, null=True)

    referred_by = models.CharField(
        max_length=50,
        choices=Choices(
            ('ngo', _('Through an NGO')),
            ('sports_ngo', _('Through a Sports Club/NGO')),
            ('friends', _("Through friends")),
            ('others', _("Others")),
        ),
        blank=True, null=True
    )
    communication_preference = models.CharField(
        max_length=50,
        choices=Choices(
            ('facebook', _('Facebook')),
            ('email', _('E-mail')),
            ('mobile', _("Mobile")),
            ('ngo', _("Through the NGO partner")),
            ('none', _("I don't want follow up")),
        ),
        blank=True, null=True
    )

    communication_channel = models.CharField(
        max_length=50,
        blank=True, null=True
    )

    class Meta:
        ordering = ['first_name']
        verbose_name = _("Youth")
        verbose_name_plural = _("Youth")

    def get_absolute_url(self):
        return reverse('youth:edit', kwargs={'pk': self.id})
