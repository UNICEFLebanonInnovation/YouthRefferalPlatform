from django.db import models
from django.contrib.postgres.fields import JSONField

from model_utils import Choices

from referral_platform.locations.models import Location
from referral_platform.youth.models import YoungPerson
from referral_platform.partners.models import PartnerOrganization


class Lab(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Path(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    path = models.ForeignKey(Path, blank=True, null=True, related_name='courses')
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

    def total_enrolled(self):
        self.enrollment_set.count()


class Enrollment(models.Model):

    STATUS = Choices(
        'enrolled',
        'pre_test',
        'post_test'
    )

    youth = models.ForeignKey(YoungPerson)
    course = models.ForeignKey(Course, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    status = models.CharField(max_length=50, choices=STATUS, default=STATUS.enrolled)
    pre_test = JSONField(blank=True, null=True)
    post_test = JSONField(blank=True, null=True)

    scores = JSONField(blank=True, null=True, default=dict)

    class Meta:
        ordering = ['id']

    def score(self, indicator, stage, keys, weight=100):

        assessment = getattr(self, stage, 'pre_test')

        marks = {key: int(assessment.get(key, 0)) for key in keys}

        maximum = 5 * len(keys)
        total = sum(marks.values())
        score = (float(total) / float(maximum)) * weight
        self.scores['{}_{}'.format(indicator, stage)] = score

        pre_test_score = self.scores.get('{}_{}'.format(indicator, 'pre_test'), 0)
        post_test_score = self.scores.get('{}_{}'.format(indicator, 'post_test'), 0)
        self.scores['{}_{}'.format(indicator, 'improved')] = post_test_score > pre_test_score


