# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportMixin
from mptt.admin import MPTTModelAdmin

from .models import (
    Location,
    LocationType,
)


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        fields = (
            'id',
            'name',
            'type',
            'latitude',
            'longitude',
            'p_code',
            'parent',
        )
        export_order = ('name', )


class LocationAdmin(ImportExportMixin, MPTTModelAdmin):
    resource_class = LocationResource
    list_display = (
        'name',
        'type',
        'parent',
    )
    list_filter = (
        'type',
    )
    search_fields = (
        'name',
    )


admin.site.register(Location, LocationAdmin)
admin.site.register(LocationType)

