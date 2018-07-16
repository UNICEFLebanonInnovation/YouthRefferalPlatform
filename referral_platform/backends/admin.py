# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from django.contrib.admin.models import LogEntry

from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import Exporter


class ExporterResource(resources.ModelResource):
    class Meta:
        model = Exporter


class ExporterAdmin(ImportExportModelAdmin):
    resource_class = ExporterResource
    list_display = (
        'name',
        'partner',
        'created',
        'file_url',
    )

    def get_export_formats(self):
        from .utils import get_default_export_formats
        return get_default_export_formats()


admin.site.register(LogEntry)
admin.site.register(Exporter, ExporterAdmin)
