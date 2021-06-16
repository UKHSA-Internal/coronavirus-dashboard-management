#!/usr/bin python3

from django.contrib import admin

from ...models.metric_docs import MetricAsset, MetricAssetToMetric
from ..generic_admin import GuardedAdmin
from ..mixins import ProdOnlyOps


__all__ = [
    'MetricAssetAdmin'
]


class MetricInlineAdmin(admin.TabularInline):
    model = MetricAssetToMetric
    can_delete = False
    readonly_fields = ['id']


@admin.register(MetricAsset)
class MetricAssetAdmin(ProdOnlyOps, GuardedAdmin):
    search_fields = ('label',)
    readonly_fields = ['id', 'last_modified']
    inlines = (MetricInlineAdmin,)
    list_display = [
        'label',
        'released',
        'last_modified',
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'last_modified',
                    'label',
                    'released',
                    'body'
                ),
            },
        ),
    )
