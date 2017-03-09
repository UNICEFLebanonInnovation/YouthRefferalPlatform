
from django.db import models


class PartnerOrganization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    overview = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Course(models.Model):

    partner = models.ForeignKey(PartnerOrganization)
    name = models.CharField(max_length=100)
    overview = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.IntegerField()
