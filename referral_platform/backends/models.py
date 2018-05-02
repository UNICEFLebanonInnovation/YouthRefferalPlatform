from __future__ import unicode_literals, absolute_import, division

from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.gis.db import models

from model_utils.models import TimeStampedModel

from referral_platform.partners.models import PartnerOrganization


class Exporter(TimeStampedModel):

    name = models.CharField(max_length=100)
    partner = models.ForeignKey(
        PartnerOrganization,
        blank=True, null=True,
        related_name='+',
        verbose_name=_('Partner organization'),
    )
    exported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False, null=True,
        related_name='+',
    )
    file_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['created']
        verbose_name = "Exported file"
        verbose_name_plural = "Exported files"

    def __unicode__(self):
        return self.name
