
from django.db import models


class PartnerOrganization(models.Model):
    name = models.CharField(max_length=100L, unique=True)

    def __unicode__(self):
        return self.name
