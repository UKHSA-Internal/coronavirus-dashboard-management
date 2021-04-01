#!/usr/bin python3

from django.contrib import admin

from ...models.metric_docs import MetricDescription
from ..generic_admin import GuardedAdmin


__all__ = [
    'MetricDescriptionAdmin'
]


@admin.register(MetricDescription)
class MetricDescriptionAdmin(GuardedAdmin):
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
                    'description'
                ),
            },
        ),
    )


