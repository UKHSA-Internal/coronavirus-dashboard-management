#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:

# 3rd party:
from django.contrib.admin import TabularInline

# Internal: 
from service_admin.models.change_log import ChangeLog

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ChangeLogMetricsAdmin',
    'ChangeLogPagesAdmin'
]


class ChangeLogMetricsAdmin(TabularInline):
    verbose_name = "Metric association"
    verbose_name_plural = "Metric associations"
    model = ChangeLog.metrics.through
    readonly_fields = ['id']
    extra = 20


class ChangeLogPagesAdmin(TabularInline):
    verbose_name = "Page association"
    verbose_name_plural = "Page associations"
    model = ChangeLog.pages.through
    readonly_fields = ['id']
    extra = 5
