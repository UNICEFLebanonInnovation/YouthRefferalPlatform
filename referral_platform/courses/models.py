from django.db import models

from referral_platform.youth.models import YoungPerson


class Lab(models.Model):
    name = models.CharField(max_length=100)


class Course(models.Model):
    name = models.CharField(max_length=100)


class Enrollment(models.Model):

    youth = models.ForeignKey(YoungPerson)
    course = models.ForeignKey(Course, blank=True, null=True)
    lab = models.ForeignKey(Lab, blank=True, null=True)
