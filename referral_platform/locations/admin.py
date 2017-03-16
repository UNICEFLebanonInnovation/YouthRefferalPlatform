# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from import_export import resources, fields
from import_export import fields
from import_export.admin import ImportExportModelAdmin

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
            'p_code'
        )
        export_order = ('name', )


class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = (
        'name', 'parent'
    )

admin.site.register(Location, LocationAdmin)
admin.site.register(LocationType)

