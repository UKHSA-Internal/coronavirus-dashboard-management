#!/usr/bin python3

from django.contrib import admin
from reversion.admin import VersionAdmin

from ..models.data import AreaReference
from .generic_admin import GuardedAdmin
from .mixins import ProdOnlyOps


__all__ = [
    'AreaReferenceAdmin'
]


@admin.register(AreaReference)
class AreaReferenceAdmin(VersionAdmin, GuardedAdmin):
    search_fields = ('area_type', 'area_name', 'area_code')
    list_per_page = 100
    ordering = ('area_name', 'area_type')
    readonly_fields = ['id']
    list_display = [
        'area_name',
        'area_type',
        'area_code',
    ]
    list_filter = [
        'area_type'
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    ('area_type', 'area_name', 'area_code'),
                ),
            },
        ),
    )
