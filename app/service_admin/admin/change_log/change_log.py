#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib import admin

# Internal: 
from ...models.change_log import ChangeLog

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLogAdmin'
]


class ChangeLogMetricsAdmin(admin.TabularInline):
    verbose_name = "Metric association"
    verbose_name_plural = "Metric associations"
    model = ChangeLog.metrics.through
    readonly_fields = ['id']
    extra = 10


class ChangeLogPagesAdmin(admin.TabularInline):
    verbose_name = "Page association"
    verbose_name_plural = "Page associations"
    model = ChangeLog.pages.through
    readonly_fields = ['id']
    extra = 5


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    search_fields = [
        'heading'
    ]

    readonly_fields = [
        'id'
    ]

    list_display = [
        "heading",
        "date",
        "expiry",
        "high_priority",
        "type"
    ]

    inlines = [ChangeLogPagesAdmin, ChangeLogMetricsAdmin]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'id',
                    'type',
                    ('display_banner', 'high_priority'),
                    ('date', 'expiry'),
                    'heading',
                    'body',
                    'details',
                ),
            },
        ),
    )