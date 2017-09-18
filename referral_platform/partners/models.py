
from django.db import models
from referral_platform.locations.models import Location


class PartnerOrganization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=15,
        null=True,
        blank=True
    )
    overview = models.TextField(null=True, blank=True)
    locations = models.ManyToManyField(Location, blank=True)

    def __unicode__(self):
        return self.name

