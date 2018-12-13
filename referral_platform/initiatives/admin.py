import tablib


from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from import_export.widgets import *
from django.utils.translation import ugettext as _

from referral_platform.users.utils import has_group, force_default_language
from referral_platform.locations.models import Location
from referral_platform.partners.models import PartnerOrganization
from .models import YouthLedInitiative

admin.site.register(YouthLedInitiative)
