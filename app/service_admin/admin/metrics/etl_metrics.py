#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin

# Internal:
from ..generic_admin import GuardedAdmin
from ...models import MetricETLReference

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'MetricETLReferenceAdmin'
]


@admin.register(MetricETLReference)
class MetricETLReferenceAdmin(GuardedAdmin):
    search_fields = ('metric',)
    list_per_page = 100
    ordering = ('metric',)
    readonly_fields = ['id']
    list_display = [
        'metric',
        'missing_to_zero',
        'fill_forward',
        'negative_to_zero',
        'prevalence_rate',
        'incidence_rate',
        'ratio_to_percentage',
        'rolling_sum_direction',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'metric',
                    ('missing_to_zero', 'fill_forward', 'negative_to_zero'),
                    ('prevalence_rate', 'incidence_rate', 'ratio_to_percentage'),
                    'rolling_sum_direction',
                ),
            },
        ),
    )
