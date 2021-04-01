#!/usr/bin python3

from django.contrib import admin

from ...models.metric_docs import MetricMethodology
from ..generic_admin import GuardedAdmin


__all__ = [
    'MetricMethodologyAdmin'
]


@admin.register(MetricMethodology)
class MetricMethodologyAdmin(GuardedAdmin):
    search_fields = ('label',)
    readonly_fields = ['id']

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'label',
                    'metric',
                    'methodology'
                ),
            },
        ),
    )
