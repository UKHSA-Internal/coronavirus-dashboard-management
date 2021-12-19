#!/usr/bin python3

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Python:
from datetime import timedelta, datetime
import re

# 3rd party:
from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.utils import timezone
from django.db.models import DateTimeField
from django.conf import settings

from azure.cosmosdb.table.tableservice import TableService

from reversion.admin import VersionAdmin

from django_object_actions import DjangoObjectActions

# Internal:
from service_admin.models.data import ReleaseReference, Despatch, DespatchToRelease, PROCESS_TYPE_ENUM, ProcessedFile
from service_admin.admin.generic_admin import GuardedAdmin
from service_admin.utils.presets import ServiceName
from service_admin.utils.dispatch_ops import update_timestamps
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


__all__ = [
    'ReleaseReferenceAdmin',
    'DateTimeFilter'
]


SERVICE_NAME = getattr(ServiceName, settings.ENVIRONMENT)


def release_selected(modeladmin, request, queryset):
    timestamp = datetime.utcnow()
    queryset.update(released=True)

    despatch = Despatch.objects.create(timestamp=timestamp)

    new_objects = list()

    for release in queryset:
        DespatchToRelease.objects.filter(release=release).delete()
        new_objects.append(DespatchToRelease(despatch=despatch, release=release))

    DespatchToRelease.objects.bulk_create(new_objects)

    update_timestamps(timestamp)


release_selected.short_description = f"Release selected deployments on {SERVICE_NAME.capitalize()}"


class FilterByReleaseCategory(admin.SimpleListFilter):
    title = _('release category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return PROCESS_TYPE_ENUM

    def queryset(self, request, queryset):
        value = self.value()

        if value:
            return queryset.filter(category__process_name=value)

        return queryset


class FilterByReleaseStatus(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('release status')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        lookup = [
            ("released", _("Released")),
            ("pending", _("Pending")),
        ]

        return lookup

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()

        if value == 'release':
            queryset = queryset.filter(release_id__released=True)
        elif value == 'pending':
            queryset = queryset.filter(release_id__released=False)

        return queryset


class DateTimeFilter(admin.DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        if isinstance(field, DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:       # field is a models.DateField
            today = now.date()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        self.links = (
            (_('Any date'), {}),
            (_('Today'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Yesterday'), {
                self.lookup_kwarg_since: str(yesterday),
                self.lookup_kwarg_until: str(today),
            }),
            (_('Today and yesterday'), {
                self.lookup_kwarg_since: str(yesterday),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            *self.links[2:]
        )


@admin.register(ReleaseReference)
class ReleaseReferenceAdmin(VersionAdmin, DjangoObjectActions, GuardedAdmin):
    table_obj = TableService(connection_string=settings.ETL_STORAGE)

    search_fields = ('label',)
    list_per_page = 30
    readonly_fields = ["category"]
    actions = [release_selected]
    list_filter = [
        FilterByReleaseStatus,
        FilterByReleaseCategory,
        ('timestamp', DateTimeFilter)
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
