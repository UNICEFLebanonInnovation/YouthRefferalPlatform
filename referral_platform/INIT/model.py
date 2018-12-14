from django.db import models
from django.contrib.postgres.fields import JSONField

from model_utils import Choices

from referral_platform.locations.models import Location
from referral_platform.youth.models import YoungPerson
from referral_platform.partners.models import PartnerOrganization


class YLInitiative(models.Model):

    owner = models.ForeignKey(PartnerOrganization, blank=True, null=True)
    name = models.CharField(max_length=100)
    overview = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    assessment_form = models.URLField(blank=True, null=True)
    members = models.ForeignKey(YoungPerson)
    location = models.ForeignKey(Location, blank=True, null=True)

    class Meta:
        ordering = ['id']



