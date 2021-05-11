#!/usr/bin python3

from django.contrib import admin

from ..models.data import AreaReference
from .generic_admin import GuardedAdmin
from .mixins import ProdOnlyOps


__all__ = [
    'AreaReferenceAdmin'
]


@admin.register(AreaReference)
class AreaReferenceAdmin(GuardedAdmin):
    search_fields = ('area_type', 'area_name', 'area_code')
    list_per_page = 100
    ordering = ('area_name', 'area_type')
    readonly_fields = ['id']
    list_display = [
        'area_name',
        'area_type',
        'area_code',
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
