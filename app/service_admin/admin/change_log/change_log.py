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
    model = ChangeLog.metrics.through
    readonly_fields = ['id']
    extra = 5


class ChangeLogPagesAdmin(admin.TabularInline):
    model = ChangeLog.pages.through
    readonly_fields = ['id']
    extra = 1


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
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
                    'high_priority',
                    ('date', 'expiry'),
                    'heading',
                    'body',
                    'details',
                ),
            },
        ),
    )