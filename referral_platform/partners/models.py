
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
    dashboard_url = models.CharField(max_length=1000, null=True, blank=True)

    @property
    def locations_list(self):
        if self.locations.all():
            return '\r\n'.join([f.name for f in self.locations.all()])
        return ''

    def __unicode__(self):
        return self.name

    def __iter__(self):
        return iter([self.name,
                self.phone_number,
                self.email,
                self.overview,
                self.locations])


class Center(models.Model):
    name = models.CharField(max_length=64)
    partner_organization = models.ForeignKey(PartnerOrganization, blank=False, null=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Center'

    def __unicode__(self):
        return self.name


