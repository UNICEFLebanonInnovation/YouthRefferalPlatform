from django.db import models
from django.contrib.postgres.fields import JSONField

from referral_platform.locations.models import Location
from referral_platform.youth.models import YoungPerson


class Lab(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Course(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Enrollment(models.Model):

    youth = models.ForeignKey(YoungPerson)
    course = models.ForeignKey(Course, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    pre_test = JSONField()
    post_test = JSONField()

    class Meta:
        ordering = ['id']
