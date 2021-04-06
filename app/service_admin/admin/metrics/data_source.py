#!/usr/bin python3

from django.contrib import admin

from ...models.metric_docs import MetricDataSource
from ..generic_admin import GuardedAdmin
from ..mixins import ProdOnlyOps


__all__ = [
    'MetricDataSourceAdmin'
]


@admin.register(MetricDataSource)
class MetricDataSourceAdmin(ProdOnlyOps, GuardedAdmin):
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


