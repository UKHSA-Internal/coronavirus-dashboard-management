#!/usr/bin python3

from django.contrib import admin

from ...models.metric_docs import MetricAsset, MetricAssetToMetric
from ...models.data import MetricReference
from ..generic_admin import GuardedAdmin


__all__ = [
    'MetricAssetAdmin'
]


class MetricInlineAdmin(admin.TabularInline):
    model = MetricAsset.metric.through
    can_delete = False
    readonly_fields = ['id']


@admin.register(MetricAsset)
class MetricAssetAdmin(GuardedAdmin):
    search_fields = ('label',)
    readonly_fields = ['id']
    inlines = (MetricInlineAdmin,)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'label',
                    'body'
                ),
            },
        ),
    )



