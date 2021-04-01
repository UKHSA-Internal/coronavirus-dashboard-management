#!/usr/bin python3

from django.contrib import admin

from ...models.metric_docs import MetricDataSource
from ..generic_admin import GuardedAdmin


__all__ = [
    'MetricDataSourceAdmin'
]


@admin.register(MetricDataSource)
class MetricDataSourceAdmin(GuardedAdmin):
    search_fields = ('label',)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'label',
                    'metric',
                    'applicable_to',
                    'source'
                ),
            },
        ),
    )


