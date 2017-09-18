from __future__ import unicode_literals, absolute_import, division

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import ArrayField

from model_utils import Choices
from model_utils.models import TimeStampedModel
from .utils import *
from datetime import date
import datetime


class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset()


class Student2ndShiftManager(models.Manager):
    def get_queryset(self):
        return super(Student2ndShiftManager, self).get_queryset().filter(
            student_enrollment__isnull=False,
            student_enrollment__deleted=False,
            student_enrollment__dropout_status=False,
        )


class StudentALPManager(models.Manager):
    def get_queryset(self):
        return super(StudentALPManager, self).get_queryset().filter(
            alp_enrollment__isnull=False,
            alp_enrollment__deleted=False,
            alp_enrollment__dropout_status=False
        )


class Nationality(models.Model):
    name = models.CharField(max_length=45, unique=True)
    code = models.CharField(max_length=5, null=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Nationalities"

    def __unicode__(self):
        return self.name


class IDType(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = "ID Type"

    def __unicode__(self):
        return self.name


class Labour(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Labour"

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
        ('Male', _('Male')),
        ('Female', _('Female')),
    )
    FAMILY_STATUS = Choices(
        ('married', _('Married')),
        ('engaged', _('Engaged')),
        ('divorced', _('Divorced')),
        ('widower', _('Widower')),
        ('single', _('Single')),
    )

    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    father_name = models.CharField(max_length=64, blank=True, null=True)
    # full_name = models.CharField(max_length=225L, blank=True, null=True)
    mother_fullname = models.CharField(max_length=64, blank=True, null=True)
    mother_firstname = models.CharField(max_length=64, blank=True, null=True)
    mother_lastname = models.CharField(max_length=64, blank=True, null=True)
    sex = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=GENDER
    )
    birthday_year = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        default=0,
        choices=((str(x), x) for x in range(1930, 2051))
    )
    birthday_month = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        default=0,
        choices=MONTHS
    )
    birthday_day = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        default=0,
        choices=((str(x), x) for x in range(1, 33))
    )
    family_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=FAMILY_STATUS
    )
    have_children = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices((1, _("Yes")), (0, _("No")))
    )
    phone = models.CharField(max_length=64, blank=True, null=True)
    phone_prefix = models.CharField(max_length=10, blank=True, null=True)
    registered_in_unhcr = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=Choices((1, _("Yes")), (0, _("No")))
    )
    id_number = models.CharField(max_length=45, blank=True, null=True)
    id_type = models.ForeignKey(
        IDType,
        blank=True, null=True,
    )
    nationality = models.ForeignKey(
        Nationality,
        blank=True, null=True,
        related_name='+'
    )
    mother_nationality = models.ForeignKey(
        Nationality,
        blank=True, null=True,
        related_name='+'
    )
    address = models.TextField(
        blank=True,
        null=True
    )
    p_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    number = models.CharField(max_length=45, blank=True, null=True)
    number_part1 = models.CharField(max_length=45, blank=True, null=True)
    number_part2 = models.CharField(max_length=45, blank=True, null=True)

    def __unicode__(self):
        if not self.first_name:
            return 'No name'

        return u'{} {} {}'.format(
            self.first_name,
            self.father_name,
            self.last_name,
        )

    @property
    def full_name(self):
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

    @property
    def age(self):
        current_year = datetime.datetime.now().year
        if self.birthday_year:
            return int(current_year)-int(self.birthday_year)
        return 0

    @property
    def calculate_age(self):
        today = date.today()
        years_difference = today.year - int(self.birthday_year)
        is_before_birthday = (today.month, today.day) < (int(self.birthday_month), int(self.birthday_day))
        elapsed_years = years_difference - int(is_before_birthday)
        return elapsed_years

    @property
    def phone_number(self):
        return '{}-{}'.format(self.phone_prefix, self.phone)

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
                self.mother_fullname,
                self.sex,
                self.birthday_day,
                self.birthday_month,
                self.birthday_year
            )

        super(Person, self).save(**kwargs)


class Student(Person):
    from referral_platform.outreach.models import Child

    status = models.BooleanField(default=True)
    outreach_child = models.ForeignKey(
        Child,
        blank=True, null=True,
    )

    objects = StudentManager()
    second_shift = Student2ndShiftManager()
    alp = StudentALPManager()

    @property
    def last_enrollment(self):
        return self.student_enrollment.all().last

    @property
    def last_alp_registration(self):
        return self.alp_enrollment.all().last

    @property
    def last_alp_round(self):
        registry = self.last_alp_registration()
        if registry:
            return registry.alp_round.name
        return None

    @property
    def last_alp_level(self):
        registry = self.last_alp_registration()
        if registry:
            return registry.registered_to_level.name
        return None

    @property
    def last_alp_section(self):
        registry = self.last_alp_registration()
        if registry:
            return registry.section.name
        return None

    @property
    def last_alp_referral_level(self):
        registry = self.last_alp_registration()
        if registry:
            return registry.refer_to_level.name
        return None

    @property
    def attendance_list(self):
        attendances = {}
        for item in self.attendances.all():
            attendances[item.attendance_date] = item.status
        return attendances

    def get_absolute_url(self):
        return 'student/%d' % self.pk


class StudentMatching(models.Model):

    registry = models.ForeignKey(
        Student,
        blank=False, null=False,
        related_name='+',
    )
    enrolment = models.ForeignKey(
        Student,
        blank=False, null=False,
        related_name='+',
    )
