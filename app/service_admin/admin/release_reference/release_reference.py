#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
import re

# 3rd party:
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.conf import settings

from azure.cosmosdb.table.tableservice import TableService

from reversion.admin import VersionAdmin

from django_object_actions import DjangoObjectActions

# Internal:
from . import actions, list_filters
from service_admin.models import ReleaseReference, ProcessedFile
from service_admin.admin.generic_admin import GuardedAdmin
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'ReleaseReferenceAdmin'
]


@admin.register(ReleaseReference)
class ReleaseReferenceAdmin(VersionAdmin, DjangoObjectActions, GuardedAdmin):
    table_obj = TableService(connection_string=settings.ETL_STORAGE)
    date_hierarchy = 'timestamp'

    search_fields = ('label',)
    list_per_page = 30
    readonly_fields = ["category"]
    actions = [
        actions.release_selected,
        actions.recalculate_selected_count
    ]
    list_filter = [
        list_filters.FilterByReleaseStatus,
        list_filters.FilterByReleaseCategory,
        ('timestamp', list_filters.DateTimeFilter)
    ]

    list_display = [
        'id',
        'formatted_release_time',
        'average_ts',
        'category',
        'etl_status',
        'count',
        'delta',
        'released',
        'despatch_time'
    ]

    list_display_links = [
        'formatted_release_time'
    ]

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'timestamp',
                    'released',
                    'category'
                ),
            },
        ),
    )

    def formatted_release_time(self, obj):
        return mark_safe(obj.timestamp.strftime("%a, %d %b %Y &ndash; %H:%M:%S"))

    formatted_release_time.admin_order_field = 'timestamp'
    formatted_release_time.short_description = 'receipt time'

    def despatch_time(self, obj):
        try:
            return obj.despatch_of.order_by("-timestamp").last()
        except (ValueError, AttributeError):
            return None

    despatch_time.admin_order_field = 'despatch time'
    despatch_time.short_description = 'despatch time'

    def average_ts(self, obj):

        file_path = static(
            re.sub(
                r"[:\s'\"&]+",
                "_",
                f'releases/{obj.category.process_name}/{obj.timestamp:%Y-%m-%d}.png'
            )
        )

        return mark_safe(
            f'<img src="{file_path}" loading="lazy" width="180" '
            f'style="margin-top: -10px; margin-bottom: -10px;"/>'
        )

    average_ts.admin_order_field = 'Relative receipt time'
    average_ts.short_description = 'Relative receipt time'

    def etl_status(self, obj):
        try:
            process_id = (
                ProcessedFile
                .objects
                .filter(release=obj.id)
                .order_by("timestamp")
                .last()
                .process_id
            )
        except AttributeError:
            return None

        data = self.table_obj.query_entities(
            settings.ETL_STORAGE_TABLE_NAME,
            filter=f"PartitionKey eq '{process_id}'",
        )

        for task in data:
            if task.RuntimeStatus == 'Completed':
                return mark_safe(f'<strong style="color: #074428">{task.RuntimeStatus}</strong>')
            elif task.RuntimeStatus == 'Running':
                return mark_safe(f'<strong style="color: #000044">{task.RuntimeStatus}</strong>')
            elif task.RuntimeStatus == 'Failed':
                return mark_safe(f'<strong style="color: #900000">{task.RuntimeStatus}</strong>')
            else:
                return task.RuntimeStatus

    etl_status.admin_order_field = 'ETL Status'
    etl_status.short_description = 'ETL Status'
